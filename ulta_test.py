treasury_leg= strategy({
	'strategy_name': 'rotator_leg_1',
	'underlying': 'ULTAUS5D',
	'calendar': 'common_dates',
	'signal': None, 
	'event': None, 
	'rebalancing_dates': None,
	'weight_allocation': None,
	'vol_control': {}
	})

fund_leg= strategy({
	'strategy_name': 'rotator_leg_2',
	'underlying': ['A', 'B', 'C', 'D'],
	'calendar': 'common_dates',
	'signal': None,
	'event': even.series_start,
	'rebalancing_dates': calendar.schedule({'start': xxx, 'end': yyy, freq: 'Y', adj_forward=True),  ## object where calendar will be passed on from the object
	'weight_allocation': wgt_alloc.equal_weight,
	'vol_control': {}
	})

rotator_index = strategy({
	'strategy_name': 'ULTABFR1',
	'underlying': [fund_leg, treasury_leg],
	'calendar': 'all_dates',
	'signal': None,
	'event': [{'event': [mv_avg, mv_avg], 'weight': [1,-1], 'args' = [(15,),(60,)]}, None]
	'rebalancing_dates': None
	'weight_allocation': wgt_alloc.event_allocation,
	'vol_control': None
	})
