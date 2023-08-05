rm -r ./CI
rm -r ./CD
rm -r ./vegaml
rm -r ./vega_extension
rm -r ./contrib
rm -r ./roma
rm -r ./examples/compression/prune_ea/prune_mobilenet.yml
rm -r ./examples/compression/quant_ea/quant_ea_mobile.yml
rm -r ./examples/fully_train/edvr
rm -r ./examples/fully_train/faster_rcnn
rm -r ./examples/fully_train/nasbench
rm -r ./examples/fully_train/resnet_md
rm -r ./examples/fully_train/transformer
rm -r ./examples/nas/gdas
rm -r ./examples/nas/sgas
rm -r ./examples/nas/sm_nas
rm -r ./examples/developer
rm -r ./vega/networks/vit.py
rm -r ./vega/networks/pytorch/transformer
rm -rf ./vega/op_search
rm -rf ./docs/cn/user/network_train_tricks.md

# do security changes
cp -f ./vega/security/config_op.py ./vega/tools/config_op.py
cp -f ./vega/security/rest.py ./vega/evaluator/tools/rest.py
cp -f ./vega/security/run_dask.py ./vega/core/scheduler/run_dask.py
cp -f ./vega/security/run_flask.py ./evaluate_service/run_flask.py
cp -f ./vega/security/run_pipeline.py ./vega/tools/run_pipeline.py
cp -f ./vega/security/query_process.py ./vega/tools/query_process.py
cp -f ./vega/security/query_progress.py ./vega/tools/query_progress.py
cp -f ./vega/security/kill.py ./vega/tools/kill.py
cp -f ./vega/security/setup.py ./setup.py
cp -f ./vega/security/main.py ./evaluate_service/main.py
rm -rf ./vega/security

# get version
version="1.8.0.mindstudio"
version=$version$(date "+%Y%m%d")
# chang setup.py version
str="    version=\""$version"\", "
sed -i "s/.*version=.*/$str/" ./setup.py
# change vega version
str="__version__ = \""$version"\""
sed -i "s/.*__version__.*/$str/" ./vega/__init__.py
python3 ./setup.py bdist_wheel sdist
