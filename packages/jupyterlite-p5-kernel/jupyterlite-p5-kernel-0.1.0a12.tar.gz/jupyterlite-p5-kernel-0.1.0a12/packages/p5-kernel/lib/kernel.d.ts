import { KernelMessage } from '@jupyterlab/services';
import { IKernel } from '@jupyterlite/kernel';
import { JavaScriptKernel } from '@jupyterlite/javascript-kernel';
/**
 * A kernel that executes code in an IFrame.
 */
export declare class P5Kernel extends JavaScriptKernel implements IKernel {
    /**
     * Instantiate a new P5Kernel.
     *
     * @param options The instantiation options for a new P5Kernel.
     */
    constructor(options: P5Kernel.IOptions);
    /**
     * A promise that is fulfilled when the kernel is ready.
     */
    get ready(): Promise<void>;
    /**
     * Handle a kernel_info_request message
     */
    kernelInfoRequest(): Promise<KernelMessage.IInfoReplyMsg['content']>;
    /**
     * Handle an `execute_request` message
     *
     * @param msg The parent message.
     */
    executeRequest(content: KernelMessage.IExecuteRequestMsg['content']): Promise<KernelMessage.IExecuteReplyMsg['content']>;
    /**
     * Handle magics coming from execute requests.
     *
     * @param code The code block to handle.
     */
    private _magics;
    private _bootstrap;
    private _inputs;
    private _p5Ready;
}
/**
 * A namespace for P5Kernel statics.
 */
export declare namespace P5Kernel {
    /**
     * The instantiation options for a P5Kernel
     */
    interface IOptions extends IKernel.IOptions {
        /**
         * The URL to fetch p5.js
         */
        p5Url: string;
    }
}
