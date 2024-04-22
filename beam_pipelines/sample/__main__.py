import apache_beam as beam

with beam.Pipeline() as pipeline:
    sample = (
            pipeline
            | 'Create produce' >> beam.Create([
        '🍓 Strawberry',
        '🥕 Carrot',
        '🍆 Eggplant',
        '🍅 Tomato',
        '🥔 Potato',
    ])
            | 'Sample N elements' >> beam.combiners.Sample.FixedSizeGlobally(3)
            | beam.Map(print))
