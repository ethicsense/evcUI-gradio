import gradio as gr
import sys
import argparse
import os
# import runEVCgradio as evc


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


def test(url, account, group, node, ip, port, owner, model_name, task, version, mode, app, server_port):
    default_set, default_cfg, modelfile, dockerfile = evc.get_myprj(url, account)

    for run in default_cfg:
        sequence = run['activation']

        if sequence == 'register':
            builders = evc.device_control.host_config(default_set, group, node, ip, port, owner)
        
        elif sequence == 'build':
            # if str2bool(clean_db):
            #     print()
            #     print()
            #     evc.clean_db()
            evc.clean_db(model_name, version)
            evc.model_control.build(
                builders, owner, model_name, task, version, modelfile, dockerfile
            )

        elif sequence == 'download':
            evc.model_control.download(
                group, owner, model_name, task, version, modelfile, dockerfile,
                server_port
            )

        elif sequence == 'run':
            out = evc.model_control.run(
                group, owner, model_name, task, version, modelfile, dockerfile,
                mode, app, server_port
            )

    return out


with gr.Blocks() as demo:
    '''
    추가된 부분 (시작)
    '''
    with gr.Row():

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a Face Detection Service. </strong>")
            sample1 = gr.Video(value="./Image/face_sample.mp4", autoplay=True)  
            face_btn = gr.Button("Deploy")

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a Fashion Detection Service. </strong>")
            sample2 = gr.Video(value="./Image/fashion_sample.mp4", autoplay=True)  
            fashion_btn = gr.Button("Deploy")

    with gr.Row():

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a HardHat Detection Service. </strong>")
            sample3 = gr.Video(value="./Image/hardhat_sample.mp4", autoplay=True)  
            hardhat_btn = gr.Button("Deploy")

        with gr.Column():
            markdown = gr.Markdown("<strong> This is a Wind Mills Detection Service. </strong>")
            sample4 = gr.Video(value="./Image/windmills_sample.mp4", autoplay=True)  
            windmill_btn = gr.Button("Deploy")

    '''
    추가된 부분 (끝)
    # 밑에 Accordion도 추가됨. (열고 닫기 기능)
    '''

    with gr.Accordion("EVC Deployment System", open=False):
        title1 = gr.Markdown(
                """
                # <center> EVC Deployment System </center>
                """
            )

        with gr.Row(): 

            with gr.Column():

                with gr.Row():
                    account = gr.Textbox(label="Github Account", scale=0)
                    url = gr.Textbox(label="Project URL")
                
                with gr.Row():
                    model_name = gr.Textbox(label="Model Name", value="esp-test")
                    version = gr.Textbox(label="Model Version", value="0.6")
                    task = gr.Textbox(label="Model Task", value="detection")
                    mode = gr.Textbox(label="Activation Mode", value="flask")
                    server_port = gr.Textbox(label="Model Application Port", value=7999)

        with gr.Row():
            title2 = gr.Markdown(
                """
                ## <center> Target Node Information </center>
                """
            )
            btn2 = gr.Button("Start Deployment", scale=0)

        with gr.Row():
            with gr.Column(scale=0, min_width=170):
                group = gr.Textbox(label="Group Name", value="keti_test_nuc")
                owner = gr.Textbox(label="Admin", value="keti")

            with gr.Row():
                node = gr.Textbox(label="Node Name", value="n02")
                ip = gr.Textbox(label="IP Address", value="evc.re.kr")
                port = gr.Textbox(label="Port Number", value=33322)
                app = gr.Textbox(label="Model App URL", value="192.168.1.5:7999")


    output = gr.Textbox(label="Result")
    btn2.click(
        test,
        [url, account, group, node, ip, port, owner, model_name, task, version, mode, app, server_port],
        output
    )

    '''
    deploy_btn을 click하면 
    "EVC Deployment System"의 url(gr.Textbox)에 지정된 깃허브 주소가 들어가도록 하는 부분입니다.
    혹시 필요하시면 참고하세요 !!

    * url = gr.Textbox(label="Project URL", value="https://github.com/ethicsense/esp-python.git") 의 value부분 지우고 사용하시면 됩니다!
    '''
    face_txt = gr.Text(visible=False, value="https://github.com/hibobo98/Face.git")
    fashion_txt = gr.Text(visible=False, value="https://github.com/hibobo98/Fashion.git")
    hardhat_txt = gr.Text(visible=False, value="https://github.com/hibobo98/Hardhat.git")
    windmill_txt = gr.Text(visible=False, value="https://github.com/hibobo98/Windmill.git")

    def same(x):
        return x
    
    face_btn.click(fn=same, inputs=[face_txt], outputs=[url])
    fashion_btn.click(fn=same, inputs=[fashion_txt], outputs=[url])
    hardhat_btn.click(fn=same, inputs=[hardhat_txt], outputs=[url])
    windmill_btn.click(fn=same, inputs=[windmill_txt], outputs=[url])






demo.queue().launch(
    server_name=args.server_name,
    server_port=args.server_port,
    debug=True
)