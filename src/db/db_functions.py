from src.db.engine_manager import EngineManager
from src.db.features_models import FeaturesCollapsedSctn, FeaturesCollapsedSttc
from src.db.features_queries import UpsertQuerySctn, UpsertQuerySttc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
import os
import pandas as pd
import tomli
from src.db.features_queries import SelectQuerySctn, SelectQuerySttc
import random

class DB_Engine:
    def __init__(self, n_sections = 8):
        self.engine_manager = None
        __loc = os.getcwd()
        with open(os.path.join(__loc, 'db_cfg.toml'), 'rb') as cfg:
            feats_db_cfg = tomli.load(cfg)['DATABASE-local']
            
            username = feats_db_cfg['USERNAME']
            password = feats_db_cfg['PASSWORD']
            host = feats_db_cfg['HOST']
            database = feats_db_cfg['DATABASE']
            port = feats_db_cfg['PORT']
            
            self.engine_manager = EngineManager(
                username=username,
                password=password,
                host=host,
                database=database,
                port=port
            )
        self.n_sections = n_sections
        self.engine = self.engine_manager.engine()

        # shared utilities
        # self.select_query_sctn_all = SelectQuerySctn(FeaturesCollapsedSctn)
        # self.select_query_sttc_all = SelectQuerySttc(FeaturesCollapsedSttc)

        self.session_maker = sessionmaker(self.engine)

    def check_if_record_exists(self, record):
        """record: string id of deezer_track
        returns bool of true or false, if the track_id is already located in the db"""
        select_query_sttc_one = SelectQuerySttc(table=FeaturesCollapsedSttc, where_col_equal=(FeaturesCollapsedSttc.track_id, record))
        # select_query_sctn_one = SelectQuerySctn(table=FeaturesCollapsedSctn, where_col_equal=(FeaturesCollapsedSctn.track_id, record))

        with self.engine.connect() as conn:
            # sctn_feats = pd.read_sql(select_query_sctn_one.select_id_feats, conn)
            sttc_feats = pd.read_sql(select_query_sttc_one.select_id_feats, conn)

        if sttc_feats.shape[0] == 0:
            # Record doesn't already exist, need to featurize
            return False
        else:
            return True
        
    def insert_record(self, track_id, features):
        """accepts features to insert into the database
        
        returns: true or false depending on whether the commit worked or not."""

        # with self.session_maker() as session:
        #     session.execute(insert(FeaturesCollapsedSctn), features.to_dict(orient='records'))
        #     session.commit()
        with self.session_maker() as session:
            for i in range(self.n_sections):
                upsert_query_sctn = UpsertQuerySctn(
                    table = FeaturesCollapsedSctn,
                    track_id = track_id,
                    section = i+1,
                    spctrl_rlf=features["collapsed_rolloff"][i].item(),
                    spctrl_cntrd=features["collapsed_centroid"][i].item(),
                    spctrl_bw=features["collapsed_bandwidth"][i].item(),
                    spctrl_cntrst=features["collapsed_contrast"][i].item(),
                    rms=features["collapsed_rms"][i].item(),
                    spctrl_flux=features["collapsed_flux"][i].item(),
                    dnmc_rng=features["collapsed_dynamic_range"][i].item(),
                    instrmntlns=features["collapsed_instrumentalness"][i].item()
                    )
                        
                print("WEEE")
                session.execute(upsert_query_sctn.upsert_id_feats)

            upsert_query_sttc = UpsertQuerySttc(
                table = FeaturesCollapsedSttc, 
                track_id = track_id,
                bpm = features["bpm"],
                keymjr = features["major_key"][:5],
                keymnr = features["minor_key"][:5]
            )
            
            print("finished running upsert stcn")
            session.execute(upsert_query_sttc.upsert_id_feats)
            print("finished running upsert sttc")
            session.commit()
            print("successful commit")
        
    def obtain_all_records(self):
        
        with self.engine.connect() as conn:
            select_query_sctn_all = SelectQuerySctn(FeaturesCollapsedSctn, None)
            select_query_sttc_all = SelectQuerySttc(FeaturesCollapsedSttc, None)
            sctn_feats = pd.read_sql(select_query_sctn_all.select_id_feats, conn)
            sttc_feats = pd.read_sql(select_query_sttc_all.select_id_feats, conn)

        sctn_feats = sctn_feats.rename(columns={'track_id': 'track_name'})
        sttc_feats = sttc_feats.rename(columns={'track_id': 'track_name'})

        feats = ('spctrl_rlf', 'spctrl_cntrd', 'spctrl_bw',
                'spctrl_cntrst', 'rms', 'spctrl_flux',
                'dnmc_rng', 'instrmntlns')

        id_cols = ('track_name', 'section')

        bigguy = sctn_feats.loc[:, id_cols + (feats[0],)].pivot(index='track_name',
                                                            columns='section',
                                                            values=feats[0]).rename(
                                                                columns={i: f'{feats[0]}_{i}' for i in range(1, self.n_sections+1)}
                                                                ).reset_index()

        for feat in feats[1:]:
            temp = sctn_feats.loc[:, id_cols + (feat,)].pivot(index='track_name',
                                                            columns='section',
                                                            values=feat).rename(
                                                                columns={i: f'{feat}_{i}' for i in range(1, self.n_sections+1)}
                                                                ).reset_index()
            bigguy = bigguy.merge(temp, on=['track_name'])

        bigguy = bigguy.merge(sttc_feats, on=['track_name'])

        return bigguy