select
    minute as "Entry Date UTC",
    price
from prices.usd
where blockchain = 'ethereum'
  and symbol = 'stETH'
  and extract(minute from minute) % 5 = 0
  and date(minute) between date '2022-01-01' and date '2022-04-30'
order by minute asc