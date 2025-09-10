from kfp.dsl import pipeline
from kubeflow.components.components import ingest_op, featurize_op, train_op, evaluate_op, register_op

@pipeline(name='forecasting-pipeline')
def forecasting_pipeline(csv_path: str = 'data/retail_sales_small.csv'):
    i=ingest_op(csv_path)
    f=featurize_op(i.output)
    t=train_op(f.output)
    e=evaluate_op(f.output, t.output)
    r=register_op(t.output)

if __name__=='__main__':
    from kfp import compiler
    compiler.Compiler().compile(forecasting_pipeline, package_path='kfp_forecasting_pipeline.json')
