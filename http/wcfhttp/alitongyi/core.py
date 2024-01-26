#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import dashscope

from fastapi import Body
from http import HTTPStatus




class TongyiApi:
    def __init__(self):
        self.LOG = logging.getLogger(__name__)
        self.LOG.info("tongyi api")

    def call_with_messages(
        u: str = Body(""),
        lastPrompt: dict = Body({}),
    ) -> dict:
        messages = []
        # print("lastPrompt", lastPrompt)
        # if "role" in lastPrompt:
        #     messages.append(lastPrompt)

        messages.append(
            {"role": "user", "content": u},
        )

        print("messages", messages)

        response = dashscope.Generation.call(
            model="baichuan2-7b-chat-v1",
            messages=messages,
            result_format="message",  # set the result to be "message" format.
        )
        if response.status_code == HTTPStatus.OK:
            content = response.output.choices[0].message.content
            role = response.output.choices[0].message.role
            return {
                "status": response.status_code,
                "role": role,
                "content": content,
                "request_id": response.request_id,
            }
        else:
            print(
                "Request id: %s, Status code: %s, error code: %s, error message: %s"
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                )
            )
            return {"status": 1, "message": response.message}

    def call_with_prompt() -> dict:
        response = dashscope.Generation.call(
            model=dashscope.Generation.Models.qwen_turbo, prompt="如何做炒西红柿鸡蛋？"
        )

        # The response status_code is HTTPStatus.OK indicate success,
        # otherwise indicate request is failed, you can get error code
        # and message from code and message.
        if response.status_code == HTTPStatus.OK:
            print(response.output)  # The output text
            print(response.usage)  # The usage information
            print(type(response))
            return {"output": response.output, "usage": response.usage}
        else:
            print(response.code)  # The error code.
            print(response.message)  # The error message.
