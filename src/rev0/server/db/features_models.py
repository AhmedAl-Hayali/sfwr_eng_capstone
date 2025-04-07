from sqlalchemy import MetaData, String, DateTime, Float, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

feats_metadata = MetaData(schema='dev')

class FeatsBase(DeclarativeBase):
    metadata = feats_metadata

class Features(FeatsBase):
    # Unused class, but may be of benefit
    __tablename__ = 'features'
    
    track_spotify_id: Mapped[str] = mapped_column(String(129), primary_key=True)
    feature_name: Mapped[str] = mapped_column(String(129), primary_key=True)
    feature_value: Mapped[str] = mapped_column(String(129))
    modtime: Mapped[datetime] = mapped_column(DateTime())
    
    def __repr__(self) -> str:
        return f'Features(track_spotify_id={self.track_spotify_id!r}, feature_name={self.feature_name!r}, feature_value={self.feature_value!r})'

class FeaturesCollapsedSctn(FeatsBase):
    __tablename__ = 'features_clpsd_sctn'
    
    track_id: Mapped[str] = mapped_column(String(129), primary_key=True)
    section: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    spctrl_rlf: Mapped[float] = mapped_column(Float)
    spctrl_cntrd: Mapped[float] = mapped_column(Float)
    spctrl_bw: Mapped[float] = mapped_column(Float)
    spctrl_cntrst: Mapped[float] = mapped_column(Float)
    rms: Mapped[float] = mapped_column(Float)
    spctrl_flux: Mapped[float] = mapped_column(Float)
    dnmc_rng: Mapped[float] = mapped_column(Float)
    instrmntlns: Mapped[float] = mapped_column(Float)
    modtime: Mapped[DateTime] = mapped_column(DateTime())
    
    def __repr__(self) -> str:
        return f'FeaturesCollapsed(track_spotify_id={self.track_spotify_id!r},section={self.section!r}, spctrl_rlf={self.spctrl_rlf!r}, spctrl_cntrd={self.spctrl_cntrd!r}, spctrl_bw={self.spctrl_bw!r}, spctrl_cntrst={self.spctrl_cntrst!r}, rms={self.rms!r}, spctrl_flux={self.spctrl_flux!r}, dnmc_rng={self.dnmc_rng!r}, instrmntlns={self.instrmntlns!r}'

class FeaturesCollapsedSttc(FeatsBase):
    __tablename__ = 'features_clpsd_sttc'
    
    track_id: Mapped[str] = mapped_column(String(129), primary_key=True)
    bpm: Mapped[int] = mapped_column(SmallInteger)
    keymjr: Mapped[str] = mapped_column(String(5))
    keymnr: Mapped[str] = mapped_column(String(5))
    modtime: Mapped[DateTime] = mapped_column(DateTime())
    
    def __repr__(self) -> str:
        return f'FeaturesCollapsed(track_spotify_id={self.track_spotify_id!r}, bpm={self.bpm!r}, keymjr={self.keymjr!r}, keymnr={self.keymnr!r})'
