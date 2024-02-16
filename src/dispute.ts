import { setMessageSendUrl } from "./chat";
import * as htmx from 'htmx.org';

let sseEventSource: EventSource;
let messageNewUuid: HTMLInputElement;

interface DisputeNewMessage {
    msg: string;
}

setMessageSendUrl('/disputes/send');

export function listenNewRoom(roomUuid: string) {
    // SSE new message
    if (sseEventSource){
        sseEventSource.close();
    }

    const channelQueryParameters = new URLSearchParams({
        channel: "room:".concat(roomUuid),
    });

    sseEventSource = new EventSource('/sse'.concat("?", channelQueryParameters.toString()));
    sseEventSource.onmessage = (evt) => {
        const newMessage = JSON.parse(evt.data) as DisputeNewMessage;
        messageNewUuid.value = newMessage.msg;
        htmx.trigger('#new_message_loader', "load_new_message");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    messageNewUuid = document.querySelector('[name="message_uuid"]');
});