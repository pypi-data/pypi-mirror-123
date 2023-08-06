/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class FileUploadConfig {
    public path: string;
    public type: 'file' | 'notebook' | 'directory';
    public mimetype: string;
    public enabled: boolean;

    constructor(map: any) {
        this.path = map.path;
        this.type = map.type || 'file';
        this.mimetype = map.mimetype || 'text/plain';
        this.enabled = map.enabled == undefined ? false : map.enabled
    }
}
