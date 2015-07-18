"""alter db

Revision ID: 2160db5051a7
Revises: 50de7a70d39a
Create Date: 2015-07-18 10:01:24.494883

"""

# revision identifiers, used by Alembic.
revision = '2160db5051a7'
down_revision = '50de7a70d39a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apscheduler_jobs')
    op.drop_column('person', 'subscriber')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('subscriber', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_table('apscheduler_jobs',
    sa.Column('id', sa.VARCHAR(length=191), autoincrement=False, nullable=False),
    sa.Column('next_run_time', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('job_state', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=u'apscheduler_jobs_pkey')
    )
    ### end Alembic commands ###