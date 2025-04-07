from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import insert, Insert
from dataclasses import dataclass, field
from datetime import datetime

from features_models import FeaturesCollapsedSctn

@dataclass
class SelectQuerySctn:
    """Query to select feature values associated with a track ID.
    
    #TODO: Docstring :)
    """
    table: str

    where_col_equal: tuple[Mapped[str], str]

    select_id_feats: Insert = field(init=False)

    def __post_init__(self):
        self.select_id_feats = select(
            self.table.track_id,
            self.table.section,
            self.table.spctrl_rlf,
            self.table.spctrl_cntrd,
            self.table.spctrl_bw,
            self.table.spctrl_cntrst,
            self.table.rms,
            self.table.spctrl_flux,
            self.table.dnmc_rng,
            self.table.instrmntlns
        )

        if self.where_col_equal is not None:
            _column = self.where_col_equal[0]
            _comparand = self.where_col_equal[1]
            self.select_id_feats = self.select_id_feats.where(_column == _comparand)


@dataclass
class SelectQuerySttc:
    """Query to select feature values associated with a track ID.
    
    #TODO: Docstring :)
    """
    table: str

    where_col_equal: tuple[Mapped[str], str] = field(init=False)

    select_id_feats: Insert = field(init=False)

    def __post_init__(self):
        self.select_id_feats = select(
            self.table.track_id,
            self.table.bpm,
            self.table.keymjr,
            self.table.keymnr
        )

        if self.where_col_equal is not None:
            _column = self.where_col_equal[0]
            _comparand = self.where_col_equal[1]
            self.select_id_feats = self.select_id_feats.where(_column == _comparand)

@dataclass
class UpsertQuerySctn:
    """Query to update (if track ID already exists) or insert feature values associated with a track ID.
    
    #TODO: Docstring :)
    """
    table: str

    track_id: str
    section: int
    spctrl_rlf: float
    spctrl_cntrd: float
    spctrl_bw: float
    spctrl_cntrst: float
    rms: float
    spctrl_flux: float
    dnmc_rng: float
    instrmntlns: float
    modtime: datetime = None

    upsert_id_feats: Insert = field(init=False)

    def __post_init__(self):
        _insert_id_feats = insert(self.table).values(
            track_id=self.track_id,
            section=self.section,
            spctrl_rlf=self.spctrl_rlf,
            spctrl_cntrd=self.spctrl_cntrd,
            spctrl_bw=self.spctrl_bw,
            spctrl_cntrst=self.spctrl_cntrst,
            rms=self.rms,
            spctrl_flux=self.spctrl_flux,
            dnmc_rng=self.dnmc_rng,
            instrmntlns=self.instrmntlns,
        )

        if self.modtime is not None:
            _insert_id_feats = _insert_id_feats.values(
                modtime=self.modtime
            )

        self.upsert_id_feats = _insert_id_feats.on_conflict_do_update(
            index_elements=[self.table.track_id],
            set_={
                self.table.track_id: _insert_id_feats.excluded.track_id,
                self.table.section: _insert_id_feats.excluded.section,
                self.table.spctrl_rlf: _insert_id_feats.excluded.spctrl_rlf,
                self.table.spctrl_cntrd: _insert_id_feats.excluded.spctrl_cntrd,
                self.table.spctrl_bw: _insert_id_feats.excluded.spctrl_bw,
                self.table.spctrl_cntrst: _insert_id_feats.excluded.spctrl_cntrst,
                self.table.rms: _insert_id_feats.excluded.rms,
                self.table.spctrl_flux: _insert_id_feats.excluded.spctrl_flux,
                self.table.dnmc_rng: _insert_id_feats.excluded.dnmc_rng,
                self.table.instrmntlns: _insert_id_feats.excluded.instrmntlns,
                self.table.modtime: _insert_id_feats.excluded.modtime
            }
        )

@dataclass
class UpsertQuerySttc:
    """Query to update (if track ID already exists) or insert feature values associated with a track ID.
    
    #TODO: Docstring :)
    """
    table: str

    track_id: str
    bpm: int
    keymjr: str
    keymnr: str
    modtime: datetime = None

    upsert_id_feats: Insert = field(init=False)

    def __post_init__(self):
        _insert_id_feats = insert(self.table).values(
            track_id=self.track_id,
            bpm=self.bpm,
            keymjr=self.keymjr,
            keymnr=self.keymnr,
        )

        if self.modtime is not None:
            _insert_id_feats = _insert_id_feats.values(
                modtime=self.modtime
            )

        self.upsert_id_feats = _insert_id_feats.on_conflict_do_update(
            index_elements=[self.table.track_id],
            set_={
                self.table.track_id: _insert_id_feats.excluded.track_id,
                self.table.bpm: _insert_id_feats.excluded.bpm,
                self.table.keymjr: _insert_id_feats.excluded.keymjr,
                self.table.keymnr: _insert_id_feats.excluded.keymnr,
                self.table.modtime: _insert_id_feats.excluded.modtime
            }
        )
