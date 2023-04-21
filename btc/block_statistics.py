from setting import ENGINE, Base  
from sqlalchemy import Column, String, Date, DATETIME, BigInteger
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.dialects.mysql import TINYINT as Tinyint
from sqlalchemy.dialects.mysql import DOUBLE as Double
  
  
class BlockStatistics(Base):  
    __tablename__ = 'block_statistics'
    height  = Column('height', Integer(unsigned=True), primary_key=True, autoincrement=False) 
    h      = Column('hash', String(64))
    dtime   = Column('time', DATETIME)
    m_dtime = Column('median_time', DATETIME)
    size    = Column('size', Integer)
    s_size  = Column('stripped_size', Integer)
    weight = Column('weight', Integer)
    v = Column('version', Integer)
    v_hex = Column('version_hex', String(8)) 
    v_bits = Column('version_bits', String(30))
    m_root = Column('merkle_root', String(64))
    nonce = Column('nonce', BigInteger)
    bits = Column('bits', BigInteger)
    difficulty = Column('difficulty', Double)
    chainwork = Column('chainwork', String(64))
    coinbase_d_hex = Column('coinbase_data_hex', String(512))
    tx_count = Column('transaction_count', Integer)
    witness_count = Column('witness_count', Integer)
    input_count = Column('input_count', Integer)
    output_count = Column('output_count', Integer)
    input_total = Column('input_total', BigInteger)
    input_total_used = Column('input_total_usd', Double)
    output_total = Column('output_total', BigInteger)
    output_total_used = Column('output_total_usd', Double)
    fee_total = Column('fee_total', BigInteger)
    fee_total_used = Column('fee_total_usd', Double)
    fee_per_kb = Column('fee_per_kb', Double)
    fee_per_kb_used = Column('fee_per_kb_usd', Double)
    fee_per_kwu = Column('fee_per_kwu', Double)
    fee_per_kwu_used = Column('fee_per_kwu_usd', Double)
    cdd_total = Column('cdd_total', Double)
    generation = Column('generation', BigInteger)
    generation_used = Column('generation_usd', Double)
    reward = Column('reward', BigInteger)
    reward_used = Column('reward_usd', Double)
    guessed_miner = Column('guessed_miner', String(512))

    def __init__(self, height, h, dtime, m_dtime, size, s_size, weight, v, v_hex, v_bits,
                 m_root, nonce, bits, difficulty, chainwork, coinbase_d_hex, tx_count, witness_count,
                 input_count, output_count, input_total, input_total_used, output_total, output_total_used,
                 fee_total, fee_total_used, fee_per_kb, fee_per_kb_used, fee_per_kwu, fee_per_kwu_used,
                 cdd_total, generation, generation_used, reward, reward_used, guessed_miner
                 ):
       self.height = height
       self.h = h
       self.dtime = dtime
       self.m_dtime = m_dtime
       self.size = size
       self.s_size = s_size
       self.weight = weight
       self.v = v
       self.v_hex = v_hex
       self.v_bits = v_bits
       self.m_root = m_root
       self.nonce = nonce
       self.bits = bits
       self.difficulty = difficulty
       self.chainwork = chainwork
       self.coinbase_d_hex = coinbase_d_hex
       self.tx_count = tx_count
       self.witness_count = witness_count
       self.input_count = input_count
       self.output_count = output_count
       self.input_total = input_total
       self.input_total_used = input_total_used
       self.output_total = output_total
       self.output_total_used = output_total_used
       self.fee_total = fee_total
       self.fee_total_used = fee_total_used
       self.fee_per_kb = fee_per_kb
       self.fee_per_kb_used = fee_per_kb_used
       self.fee_per_kwu = fee_per_kwu
       self.fee_per_kwu_used = fee_per_kwu_used
       self.cdd_total = cdd_total
       self.generation = generation
       self.generation_used = generation_used
       self.reward = reward
       self.reward_used = reward_used
       self.guessed_miner = guessed_miner

if '__main__' == __name__:
    Base.metadata.create_all(ENGINE)
  
