import gradio as gr
import sys
import argparse
import os
import runEVCv2 as evc


parser = argparse.ArgumentParser()
parser.add_argument(
    "--server_name",
    type=str,
    default="0.0.0.0"
)
parser.add_argument(
    "--server_port",
    type=int,
    default=7989
)
args=parser.parse_args()

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def test(url, mode, server_name, server_port):
    default_set, default_cfg, user_cfg, modelfile, dockerfile, mode, owner, task, version, model_name, data = evc.get_myprj(url)

    for run in default_cfg:
        sequence = run['activation']

        if sequence == 'register':
            builders = evc.device_control.host_config(default_set)
        
        elif sequence == 'build':
            # if str2bool(clean_db):
            #     print()
            #     print()
            #     evc.clean_db()
            evc.clean_db()
            evc.model_control.build(builders)

        elif sequence == 'download':
            evc.model_control.download(server_port)

        elif sequence == 'run':
            out = evc.model_control.run(mode, server_name, server_port)

    return out


with gr.Blocks() as demo:    
    with gr.Row():
        with gr.Column():
            url = gr.Textbox(label="Project URL")
            mode = gr.Textbox(label="Activation Mode")
            server_name = gr.Textbox(label="Server Name")
            server_port = gr.Textbox(label="Server Port")
        btn = gr.Button("Run", scale=0)

    output = gr.Textbox()
    btn.click(test, [url, mode, server_name, server_port], output)


demo.queue().launch(
    server_name=args.server_name,
    server_port=args.server_port,
    debug=True
)