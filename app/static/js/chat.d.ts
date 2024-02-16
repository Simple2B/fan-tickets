export declare let chatWindow: HTMLDivElement;
export declare let chatMessageContainer: HTMLDivElement;
export declare function setNewRoomUuid(roomUuid: string): void;
export declare function setMessageSendUrl(url: string): void;
export declare function toggleChatWindow(): void;
export declare let sendMessage: () => Promise<void>;
export declare function openChatWindow(): void;
export declare function createChatWindow(): void;
export declare function showMessage(): Promise<void>;
