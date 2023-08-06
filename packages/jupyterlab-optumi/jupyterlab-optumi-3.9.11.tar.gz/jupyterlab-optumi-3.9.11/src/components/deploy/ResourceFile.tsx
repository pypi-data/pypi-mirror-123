/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'

import { Checkbox, CircularProgress, IconButton, Theme, withTheme } from '@material-ui/core';
import { Global } from '../../Global';

import { FileUploadConfig } from "../../models/FileUploadConfig";

import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import CloseIcon from '@material-ui/icons/Close';
import CachedIcon from '@material-ui/icons/Cached';
import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import DirListingItemIcon from './fileBrowser/DirListingItemIcon';

interface RFProps {
    file: FileUploadConfig,
    handleFileEnabledChange: (enabled: boolean) => void,
    handleFileDelete: () => void,
    missingLocally: boolean,
    missingInCloud: boolean,
    theme: Theme,
}

interface RFState {
    hovering: boolean,
    fileSync: boolean,
}

class ResourceFile extends React.Component<RFProps, RFState> {
    _isMounted: boolean = false

    constructor(props: RFProps) {
        super(props)
        this.state = {
            hovering: false,
            fileSync: this.props.file.enabled,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const progress = Global.user.fileTracker.get(this.props.file.path);
        const compression = progress.filter(x => x.type == 'compression');
        const upload = progress.filter(x => x.type == 'upload');

        // Decide what color to make this
        // Green is if the file exists on the disk and can be synced
        // Yellow is if it doesn't exist on the disk but exists in the cloud so we can still run
        // Red is if it doesn't exist locally or in the cloud so we can't run
        // Always show is set based on color (green/gray false, red/orange true)
        const palette = this.props.theme.palette;
        var syncColor;
        var alwaysShowFileSync;
        if (this.state.fileSync) {
            if (!this.props.missingLocally) {
                syncColor = palette.success.main;
                alwaysShowFileSync = false;
            } else {
                if (!this.props.missingInCloud) {
                    syncColor = palette.warning.main;
                    alwaysShowFileSync = true;
                } else {
                    syncColor = palette.error.main;
                    alwaysShowFileSync = true;
                }
            }
        } else {
            syncColor = palette.text.disabled;
            alwaysShowFileSync = false;
        }

        return (
            <div
                style={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <div style={{
                    position: 'absolute',
                    left: '-10px',
                    paddingTop: '3px', // The checkbox is 16px, the line is 22px
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: Global.easeAnimation,
                }}>
                    <Checkbox
                        disableRipple
                        checked={this.state.fileSync}
                        style={{padding: '0px'}}
                        icon={<CheckBoxOutlineBlankIcon style={{width: '16px', height: '16px'}} />}
                        checkedIcon={<CheckBoxIcon style={{width: '16px', height: '16px'}} />}
                        onClick={() => {
                            let newFileSync = !this.state.fileSync
                            this.safeSetState({fileSync: newFileSync})
                            this.props.handleFileEnabledChange(newFileSync);
                        }}
                    />
                </div>
                <div style={{
                    position: 'absolute',
                    right: '-10px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: Global.easeAnimation,
                }}>
                    <IconButton onClick={this.props.handleFileDelete} style={{
                        width: '22px',
                        height: '22px',
                        padding: '0px',
                        position: 'relative',
                        display: 'inline-block',
                    }}>
                        <CloseIcon style={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </div>
                <div style={{
                    position: 'absolute',
                    right: '9px',
                    paddingTop: '3px', // The checkbox is 16px, the line is 22px
                    display: 'inline-flex',
                    transition: Global.easeAnimation,
                }}>
                    {(!this.props.missingLocally && (compression.length > 0 || (upload.length > 0 && upload[0].total < 0))) ? (
                        <ExtraInfo reminder={compression.length > 0 ? compression[0].total == -1 ? '' : 'Compressed ' + compression[0].progress + '/' + compression[0].total + ' files' : ''}>
                            <div style={{height: '16px', width: '16px', background: 'var(--jp-layout-color1)'}}>
                                <CircularProgress
                                    color='primary'
                                    size='14px'
                                    thickness={8}
                                    style={{margin: 'auto'}}
                                />
                            </div>
                        </ExtraInfo>
                    ) : (!this.props.missingLocally && (upload.length > 0) ? (
                        <ExtraInfo reminder={FormatUtils.styleCapacityUnitValue()(upload[0].progress) + '/' + FormatUtils.styleCapacityUnitValue()(upload[0].total)}>
                            <div style={{height: '16px', width: '16px', background: 'var(--jp-layout-color1)'}}>
                                <CircularProgress
                                    variant='determinate'
                                    size='14px'
                                    thickness={8}
                                    style={{margin: 'auto'}}
                                    value={(upload[0].progress / upload[0].total) * 100 }
                                />
                            </div>
                        </ExtraInfo>
                    ) : (
                        <CachedIcon style={{
                            position: 'relative',
                            width: '16px',
                            height: '16px',
                            transform: 'scaleX(-1)',
                            color: this.state.fileSync ? syncColor : 'var(--jp-ui-font-color2)',
                            background: 'var(--jp-layout-color1)',
                            opacity: this.state.hovering || alwaysShowFileSync ? this.state.fileSync ? '0.87' : '0.54' : '0',
                        }} />
                    ))}
                </div>
                <div
                    style={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex',
                    }}
                >
                    <DirListingItemIcon
                        fileType={this.props.file.type}
                        mimetype={this.props.file.mimetype}
                        style={{marginRight: '0px', opacity: this.state.fileSync ? '0.87' : '0.54'}}
                    />
                    <div
                        style={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            color: this.state.fileSync ? 'var(--jp-ui-font-color1)' : 'var(--jp-ui-font-color2)', // this.props.noLongerExists ? '#f48f8d' : ''
                        }}
                        title={
                            (this.props.file.path.includes('/') ? (
`Name: ${this.props.file.path.split('/').pop()}
Path: ${this.props.file.path.replace(/\/[^\/]*$/, '/')}`
                            ) : (
`Name: ${this.props.file.path.split('/').pop()}`
                            ))
                        }
                    >
                        <div style={{
                            direction: 'rtl',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                        }}>
                            {Global.convertOptumiPathToJupyterPath(this.props.file.path)}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    private handleFilesChanged = () => this.forceUpdate();

    public componentDidMount = () => {
        this._isMounted = true
        Global.user.fileTracker.getFilesChanged().connect(this.handleFilesChanged)
    }

    public componentWillUnmount = () => {
        Global.user.fileTracker.getFilesChanged().disconnect(this.handleFilesChanged)
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: RFProps, nextState: RFState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

const ThemedResourceFile = withTheme(ResourceFile)
export { ThemedResourceFile as ResourceFile }