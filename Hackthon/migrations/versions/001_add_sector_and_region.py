from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add sector and region columns to notes table
    op.add_column('note', sa.Column('sector', sa.String(length=50), nullable=False, server_default=''))
    op.add_column('note', sa.Column('region', sa.String(length=50), nullable=False, server_default=''))

def downgrade():
    # Remove sector and region columns
    op.drop_column('note', 'sector')
    op.drop_column('note', 'region')
