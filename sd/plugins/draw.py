from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
import requests
import base64
from PIL import Image
from io import BytesIO
from . import config

@on_command("画")
async def draw(session: CommandSession):
    arg = session.current_arg_text.replace("，",",")
    commands = arg.split("&")
    tags = commands[0].split(",")
    # tags = list(map(lambda x: novelai_tag_dic[x] if x in novelai_tag_dic else x, tags))
    images = session.state["images"]
    commands = commands[1:]
    d = {}
    for command in commands:
        name = command.split("=")[0]
        value = command.split("=")[1]
        d[name] = value
    # images = session.current_arg_images
    if "mode" in d:
            mode = d["mode"]
            d.pop("mode")
    else:
        if images == []:
            mode = "txt2img"
        else:
            mode = "img2img"
    if mode == "txt2img":
        url = STABLE_DIFFUSION_URL + "/sdapi/v1/txt2img"
        data = {
               #"prompt": "high quality,best quality,masterpiece,blue archive,medium breasts,tendou arisu,white hair,long hair,red eyes",
                "prompt": "best quality,{{masterpiece}}:,high quality," + ",".join(tags),
                # "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
                # "negative_prompt": "EasyNegative,multiple breasts, (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2), black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy,bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts,huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, fused ears, bad ears, poorly drawn ears, extra ears, liquid ears,leavv ears,missing ears, fused animal ears, pad animal ears,poor drawn animal ears,extra animal ears, liquid animal ears, heavy animal ears, missing animal ears, text, error, missing fingers, missing limb, fused fingers, one hand with more than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, one hand with less than 5 digit, extra digit, fewer digit, fused digit, missing digit, bad digit, lliquid digit, colorful tonque, black tongue, cropped, watermark, username, blurry, PEG artifacts, signature, malformed feet, extra feet, bad feet, poorly drawn feet, fused feet, missing feet, bad gloves, poorly drawn gloves, rused gloves,bad cum, poorly drawn cum, rused cum, ugly,missing nipples, different nipples, fused nipples, bad nipples, poorly drawn nipples, black nipples, colorful nipples, gross proportions, short arm,missing thighs, missing calf, missing legs, mutation, duplicate, morbid, mutilated, poorly drawn hands, more than 1 left hand, more than 1 right hand, deformed, (blurry), disfigured, extra arms, extra thighs, more than 2 thighs, extra calf, fused calf, extra legs, bad knee, extra knee, more than 2 legs, bad tails, bad mouth, fused mouth, poorly drawn mouth,bad tongue, black tonque, cracked mouth, bad mouth, dirty face, dirty teeth, dirty pantie, fused pantie, poorly drawn pantie, fused cloth, poorly drawn cloth, bad pantie, yellow teeth, thick lips, bad cameltoe, colorful cameltoe, bad asshole, poorly drawn asshole, fused asshole, missing asshole, bad anus, bad pussy, bad crotch, bad crotch seam,rused anus, fused pussy, fused anus, fused crotch, poorly drawn crotch, bad thigh gap, missing thigh gap, fused thigh gap, liquid thigh gap, poorly drawn thigh gap, poorly drawn anus, bad collarbone, fused collarbone, missing collarbone, liquid collarbone, strong girl, obesity, worst quality, low quality, normal quality, liquid tentacles, bad tentacles, poorly drawn tentacles, split tentacles, fused tentacles, missing clit, bad clit, fused clit, colorful clit, black clit, liquid clit, QR code, bar code, censored, safety panties, safety knickers, beard, furry, pony, pubic hair, mosaic, excrement, faeces, shit, futa, testis",
                "negative_prompt": "EasyNegative, extra fingers,fewer fingers",
                "width": 680,
                "height": 384,
                "steps":20,
                "sampler_index": "DPM++ 2M Karras",
                "enable_hr": True,
                "cfg_scale": 10,
                "denoising_strength": 0.6,
        }
    elif mode == "img2img":
        img1 = Image.open(BytesIO(requests.get(images[0]).content))
        buffer = BytesIO()
        img1.save(buffer, format="png")
        b64 = base64.b64encode(buffer.getvalue())
        url = "http://127.0.0.1:7860/sdapi/v1/img2img"
        height = (img1.height // 64) * 64
        width = (img1.width // 64) * 64
        while height < 512 and width < 512:
            height *= 2
            width *= 2
            
        data = {
                "prompt": "best quality,{{masterpiece}}:,high quality," + ",".join(tags),
                "negative_prompt": "EasyNegative,lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
                # "negative_prompt": "multiple breasts, (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2), black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy,bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts,huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, fused ears, bad ears, poorly drawn ears, extra ears, liquid ears,leavv ears,missing ears, fused animal ears, pad animal ears,poor drawn animal ears,extra animal ears, liquid animal ears, heavy animal ears, missing animal ears, text, error, missing fingers, missing limb, fused fingers, one hand with more than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, one hand with less than 5 digit, extra digit, fewer digit, fused digit, missing digit, bad digit, lliquid digit, colorful tonque, black tongue, cropped, watermark, username, blurry, PEG artifacts, signature, malformed feet, extra feet, bad feet, poorly drawn feet, fused feet, missing feet, bad gloves, poorly drawn gloves, rused gloves,bad cum, poorly drawn cum, rused cum, ugly,missing nipples, different nipples, fused nipples, bad nipples, poorly drawn nipples, black nipples, colorful nipples, gross proportions, short arm,missing thighs, missing calf, missing legs, mutation, duplicate, morbid, mutilated, poorly drawn hands, more than 1 left hand, more than 1 right hand, deformed, (blurry), disfigured, extra arms, extra thighs, more than 2 thighs, extra calf, fused calf, extra legs, bad knee, extra knee, more than 2 legs, bad tails, bad mouth, fused mouth, poorly drawn mouth,bad tongue, black tonque, cracked mouth, bad mouth, dirty face, dirty teeth, dirty pantie, fused pantie, poorly drawn pantie, fused cloth, poorly drawn cloth, bad pantie, yellow teeth, thick lips, bad cameltoe, colorful cameltoe, bad asshole, poorly drawn asshole, fused asshole, missing asshole, bad anus, bad pussy, bad crotch, bad crotch seam,rused anus, fused pussy, fused anus, fused crotch, poorly drawn crotch, bad thigh gap, missing thigh gap, fused thigh gap, liquid thigh gap, poorly drawn thigh gap, poorly drawn anus, bad collarbone, fused collarbone, missing collarbone, liquid collarbone, strong girl, obesity, worst quality, low quality, normal quality, liquid tentacles, bad tentacles, poorly drawn tentacles, split tentacles, fused tentacles, missing clit, bad clit, fused clit, colorful clit, black clit, liquid clit, QR code, bar code, censored, safety panties, safety knickers, beard, furry, pony, pubic hair, mosaic, excrement, faeces, shit, futa, testis",
                "init_images": ["data:image/png;base64," + str(b64, encoding="utf-8")],
                "height": height,
                "width": width,
        }
    # elif mode.startswith("txt2img-controlnet"):
    #     img1 = Image.open(BytesIO(requests.get(images[0]).content))
    #     buffer = BytesIO()
    #     img1.save(buffer, format="png")
    #     b64 = base64.b64encode(buffer.getvalue())
    #     url = "http://127.0.0.1:7860/controlnet/txt2img"
    #     data = {
    #            #"prompt": "high quality,best quality,masterpiece,blue archive,medium breasts,tendou arisu,white hair,long hair,red eyes",
    #             "prompt": "best quality,{{masterpiece}}:,high quality," + ",".join(tags),
    #             # "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
    #             # "negative_prompt": "EasyNegative,multiple breasts, (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2), black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy,bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts,huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, fused ears, bad ears, poorly drawn ears, extra ears, liquid ears,leavv ears,missing ears, fused animal ears, pad animal ears,poor drawn animal ears,extra animal ears, liquid animal ears, heavy animal ears, missing animal ears, text, error, missing fingers, missing limb, fused fingers, one hand with more than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, one hand with less than 5 digit, extra digit, fewer digit, fused digit, missing digit, bad digit, lliquid digit, colorful tonque, black tongue, cropped, watermark, username, blurry, PEG artifacts, signature, malformed feet, extra feet, bad feet, poorly drawn feet, fused feet, missing feet, bad gloves, poorly drawn gloves, rused gloves,bad cum, poorly drawn cum, rused cum, ugly,missing nipples, different nipples, fused nipples, bad nipples, poorly drawn nipples, black nipples, colorful nipples, gross proportions, short arm,missing thighs, missing calf, missing legs, mutation, duplicate, morbid, mutilated, poorly drawn hands, more than 1 left hand, more than 1 right hand, deformed, (blurry), disfigured, extra arms, extra thighs, more than 2 thighs, extra calf, fused calf, extra legs, bad knee, extra knee, more than 2 legs, bad tails, bad mouth, fused mouth, poorly drawn mouth,bad tongue, black tonque, cracked mouth, bad mouth, dirty face, dirty teeth, dirty pantie, fused pantie, poorly drawn pantie, fused cloth, poorly drawn cloth, bad pantie, yellow teeth, thick lips, bad cameltoe, colorful cameltoe, bad asshole, poorly drawn asshole, fused asshole, missing asshole, bad anus, bad pussy, bad crotch, bad crotch seam,rused anus, fused pussy, fused anus, fused crotch, poorly drawn crotch, bad thigh gap, missing thigh gap, fused thigh gap, liquid thigh gap, poorly drawn thigh gap, poorly drawn anus, bad collarbone, fused collarbone, missing collarbone, liquid collarbone, strong girl, obesity, worst quality, low quality, normal quality, liquid tentacles, bad tentacles, poorly drawn tentacles, split tentacles, fused tentacles, missing clit, bad clit, fused clit, colorful clit, black clit, liquid clit, QR code, bar code, censored, safety panties, safety knickers, beard, furry, pony, pubic hair, mosaic, excrement, faeces, shit, futa, testis",
    #             "negative_prompt": "EasyNegative, extra fingers,fewer fingers",
    #             "width": 1360,
    #             "height": 768,
    #             "steps":20,
    #             "sampler_index": "DPM++ 2M Karras",
    #             "enable_hr": True,
    #             "cfg_scale": 10,
    #             "denoising_strength": 0.6,
    #             "controlnet_input_image": [
    #                 "data:image/png;base64," + str(b64, encoding="utf-8")
    #             ],
    #             "controlnet_module": "openpose",
    #             "controlnet_model": "control_openpose-fp16 [9ca67cc5]"
    #     }
    #     if mode.endswith("canny"):
    #         data["controlnet_module"] = "canny"
    #         data["controlnet_model"] = "control_canny-fp16 [e3fe7712]"
    for name,value in d.items():
        if value[0].isdigit() or name == "override_settings":
            v = eval(value)
        else:
            v = value
        data[name] = v
    print(data)
    async with aiohttp.ClientSession() as _session:
            async with _session.post(url, json=data) as response:
                    content = await response.text()
                    d = json.loads(content)
                    if "detail" in d or len(d["error"]) > 2:
                        print(d)
                        await session.send("发生错误：" + d["detail"][0] if "detail" in d else d["error"])
                    else:
                        images = d["images"]
                        for i in images:
                            hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                            filename = IMAGE_DIR + "\\novelai-{}.png".format(hash)
                            with open(filename, "wb") as f:
                                f.write(base64.b64decode(i))
                            seg = MessageSegment.image("file:///" + filename)
                            pic = await session.send(seg)
    return