"""Initial database schema

Revision ID: 6cd037fbcdc6
Revises: 
Create Date: 2025-06-09 19:58:55.765911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6cd037fbcdc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('subtitle', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('features', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('currency', sa.String(length=3), server_default='RUB', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('display_order', sa.Integer(), server_default='0', nullable=False),
    sa.Column('service_type', sa.String(length=50), nullable=False),
    sa.Column('tax_type', sa.String(length=20), server_default='none', nullable=False),
    sa.Column('payment_method_type', sa.String(length=50), server_default='full_prepayment', nullable=False),
    sa.Column('payment_object_type', sa.String(length=50), server_default='service', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_name', sa.String(length=100), nullable=False),
    sa.Column('block_name', sa.String(length=100), nullable=False),
    sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('page_name', 'block_name', name='uq_page_block')
    )
    op.create_index(op.f('ix_page_content_page_name'), 'page_content', ['page_name'], unique=False)
    op.create_table('promo_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('discount_type', sa.Enum('fixed_amount', 'percentage', name='discounttype'), nullable=False),
    sa.Column('discount_value', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('usage_limit', sa.Integer(), nullable=True),
    sa.Column('used_count', sa.Integer(), server_default='0', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_promo_codes_code'), 'promo_codes', ['code'], unique=True)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('permissions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.create_table('telegram_users',
    sa.Column('telegram_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('language_code', sa.String(length=10), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=False),
    sa.Column('bot_state', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('last_interaction_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    op.create_table('admin_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('last_login_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_admin_users_username'), 'admin_users', ['username'], unique=True)
    op.create_table('customers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['telegram_id'], ['telegram_users.telegram_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=True)
    op.create_table('one_time_service_details',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=True),
    sa.Column('delivery_type', sa.String(length=50), nullable=True),
    sa.Column('delivery_content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['base_services.id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('quiz_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_user_id', sa.BigInteger(), nullable=False),
    sa.Column('responses', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('recommended_service_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('completed_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['recommended_service_id'], ['base_services.id'], ),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['telegram_users.telegram_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription_service_details',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('billing_cycle_months', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['base_services.id'], ),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('blog_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('draft', 'published', 'archived', name='blogpoststatus'), server_default='draft', nullable=False),
    sa.Column('published_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['admin_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blog_posts_slug'), 'blog_posts', ['slug'], unique=True)
    op.create_table('contact_form_submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('contact_method', sa.String(length=50), nullable=False),
    sa.Column('contact_data', sa.String(length=255), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('new', 'read', 'replied', 'archived', name='submissionstatus'), nullable=False),
    sa.Column('submitted_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('page_submitted_from', sa.String(length=255), nullable=True),
    sa.Column('replied_by_admin_id', sa.Integer(), nullable=True),
    sa.Column('replied_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['replied_by_admin_id'], ['admin_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('promo_code_id', sa.Integer(), nullable=True),
    sa.Column('quiz_session_id', sa.Integer(), nullable=True),
    sa.Column('order_status', sa.String(length=50), nullable=False),
    sa.Column('total_amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('payment_gateway', sa.String(length=50), nullable=True),
    sa.Column('gateway_invoice_id', sa.String(length=255), nullable=True),
    sa.Column('payment_transaction_id', sa.String(length=255), nullable=True),
    sa.Column('invoice_expires_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('paid_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['promo_code_id'], ['promo_codes.id'], ),
    sa.ForeignKeyConstraint(['quiz_session_id'], ['quiz_sessions.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['base_services.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gateway_invoice_id'),
    sa.UniqueConstraint('payment_transaction_id'),
    sa.UniqueConstraint('quiz_session_id')
    )
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('active', 'trial', 'past_due', 'cancelled', 'expired', name='subscriptionstatus'), nullable=False),
    sa.Column('current_period_start_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('current_period_end_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('cancelled_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('ended_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('payment_gateway_subscription_id', sa.String(length=255), nullable=True),
    sa.Column('auto_renew', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['base_services.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('payment_gateway_subscription_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    op.drop_table('orders')
    op.drop_table('contact_form_submissions')
    op.drop_index(op.f('ix_blog_posts_slug'), table_name='blog_posts')
    op.drop_table('blog_posts')
    op.drop_table('subscription_service_details')
    op.drop_table('quiz_sessions')
    op.drop_table('one_time_service_details')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_admin_users_username'), table_name='admin_users')
    op.drop_table('admin_users')
    op.drop_table('telegram_users')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_promo_codes_code'), table_name='promo_codes')
    op.drop_table('promo_codes')
    op.drop_index(op.f('ix_page_content_page_name'), table_name='page_content')
    op.drop_table('page_content')
    op.drop_table('base_services')
    # ### end Alembic commands ###
