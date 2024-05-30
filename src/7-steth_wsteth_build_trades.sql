-- USD price for stETH (or wstETH-equivalent) from multiple chains via dex trades

with
    prices as (
        select
            block_time,
            blockchain,
            project,
            case
                when
                    blockchain = 'ethereum'
                    and 0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84 in (token_bought_address, token_sold_address)
                then 'stETH'
                else 'wstETH'
            end as asset,
            case
                when (
                        blockchain = 'ethereum'
                        and token_bought_address in (
                            0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84, -- stETH ethereum
                            0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0) -- wstETH ethereum
                    ) or (
                        blockchain = 'arbitrum'
                        and token_bought_address in (
                            0x5979D7b546E38E414F7E9822514be443A4800529) -- wstETH arbitrum
                    ) or (
                        blockchain = 'polygon'
                        and token_bought_address in (
                            0x03b54a6e9a984069379fae1a4fc4dbae93b3bccd) -- wstETH polygon
                    ) or (
                        blockchain = 'optimism'
                        and token_bought_address in (
                            0x1f32b1c2345538c0c6f582fcb022739c4a194ebb) -- wstETH optimism
                    )
                    then amount_usd / token_bought_amount
                    else amount_usd / token_sold_amount
            end as usd_price
        from dex.trades
        where block_date >= cast('{{begin_date}}' as timestamp)
        and block_date <= cast('{{end_date}}' as timestamp)
        and (
                (
                    blockchain = 'ethereum'
                    and (  0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84 in (token_bought_address, token_sold_address)
                        or 0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0 in (token_bought_address, token_sold_address)
                    )
                )
            or
                (
                    blockchain = 'arbitrum'
                    and 0x5979D7b546E38E414F7E9822514be443A4800529 in (token_bought_address, token_sold_address)
                )
            or
                (
                    blockchain = 'polygon'
                    and 0x03b54a6e9a984069379fae1a4fc4dbae93b3bccd in (token_bought_address, token_sold_address)
                )
            or
                (
                    blockchain = 'optimism'
                    and 0x1f32b1c2345538c0c6f582fcb022739c4a194ebb in (token_bought_address, token_sold_address)
                )
        )
    ),
    rates as (
        select
            rebase_time_utc,
            wsteth_steth_rate
        from query_3777723 -- @lido/Reporting query MVP
    ),
    final as (
        select
            p.block_time,
            p.blockchain,
            p.project,
            p.asset,
            case when asset = 'wstETH' then usd_price / coalesce(r.wsteth_steth_rate, -1) else usd_price end as usd_price,
            r.wsteth_steth_rate
        from prices p
        left join rates r
            on date(block_time) = date(r.rebase_time_utc)
    )

select
    date_trunc('minute', block_time) as block_time,
    format('%.2f', avg(usd_price)) as usd_price
from final
where usd_price > 0
group by 1
order by block_time asc