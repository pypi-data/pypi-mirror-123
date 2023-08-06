/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import withStyles, { CSSProperties } from '@material-ui/core/styles/withStyles';
import { SubHeader } from '../../core';
import {  IconButton, Accordion, AccordionSummary, AccordionDetails, withTheme, Theme } from '@material-ui/core';
import { Global } from '../../Global';

import { NotificationsPopup } from './NotificationsPopup';
import { InfoPopup } from '../../core/InfoPoppup';
import { Packages } from './Packages';
import { ExpandMore, WarningRounded } from '@material-ui/icons';
import ExtraInfo from '../../utils/ExtraInfo';
import { Files } from './Files';

// import { EmbeddedYoutube } from '../../core/EmbeddedYoutube';

// const emDirNotFile = 'Path is a directory, not a file'
// const emDupPath = 'Duplicate file or directory'
// const emNoPath = 'Unable to find file or directory'

const StyledAccordion = withStyles({
    root: {
        borderWidth: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
        '&:before': {
            backgroundColor: 'unset',
        },
    },
})(Accordion)

const StyledAccordionSummary = withStyles({
    root: {
        padding: '0px',
        minHeight: '0px',
        '&.Mui-expanded': {
            minHeight: '0px',
        },
    },
    content: {
        margin: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
    },
    expandIcon: {
        padding: '0px',
        marginRight: '0px',
    },
})(AccordionSummary)

const StyledAccordionDetails = withStyles({
    root: {
        display: 'flex',
        flexDirection: 'column',
        padding: '0px',
    },
})(AccordionDetails)

interface IProps {
    style?: CSSProperties
    openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
    theme: Theme
}

interface IState {}

class FilesPanel extends React.Component<IProps, IState> {
    private _isMounted = false

    timeout: NodeJS.Timeout

    constructor(props: IProps) {
        super(props)
        this.state = {}
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const optumi = Global.metadata.getMetadata().config;
        const files = optumi.upload.files;
        const dataConnectors = optumi.upload.dataConnectors;
        const fileChecker = Global.user.fileChecker;
        const [yellowTriangle, redTriangle] = fileChecker.getTriangle(files, dataConnectors);
        return (
            <div style={this.props.style}>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.packagesAccordionExpanded}
                    style={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary style={{cursor: 'default'}}>
                        <div style={{display: 'flex'}}>
                            <SubHeader title='Packages'/>
                            <InfoPopup
                                title='Packages'
                                popup={
                                    <div style={{margin: '12px'}}>
                                        <p style={{whiteSpace: 'pre-line'}}>
                                            {`List python packages that your notebook imports. Optumi will pip install these packages onto the machine your session or job will run on.

                                            Each package should go on a separate line:`}
                                        </p>
                                        <img src="https://drive.google.com/uc?export=view&id=1WePvBvaS_6xgvrljKSp8iaijlnD9MFxL" width="350" />
                                        <p style={{whiteSpace: 'pre-line'}}>
                                            {`
                                            To save time you can hit the “Auto-add” button. Optumi will scan your notebook for imported packages and list them for you. However, this is a beta feature and we encourage you to double check that the list is correct.
                                            `}
                                        </p>
                                        {/* <EmbeddedYoutube
                                            name='Demo'
                                            url={'https://www.youtube.com/watch?v=MXzv-XL6LLs'}
                                            width={700}
                                            height={480}
                                        /> */}
                                    </div>
                                }
                            />
                        </div>
                        <span style={{
                            margin: 'auto 15px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.packagesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {(() => {
                                const requirements = optumi.upload.requirements
                                const numRequirements = requirements === '' ? 0 : requirements.split('\n').filter(line => line !== '').length
                                if (numRequirements > 0) {
                                    return numRequirements + ' requirement' + (numRequirements > 1 ? 's' : '')
                                }
                            })()}
                        </span>
                        <IconButton
                            onClick={() => {
                                Global.packagesAccordionExpanded = !Global.packagesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            style={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.packagesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <Packages />
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.filesAccordionExpanded}
                    style={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary style={{cursor: 'default'}}>
                        <div style={{display: 'flex'}}>
                            <SubHeader title='Files'/>
                            <InfoPopup
                                title='Files'
                                popup={
                                    <div style={{margin: '12px'}}>
                                        <p style={{whiteSpace: 'pre-line'}}>
                                            {`Upload local files and access data from supported databases. Optumi will transfer files to the machine your session or job will run on.`}
                                        </p>
                                        <img src="https://drive.google.com/uc?export=view&id=1scH_eNAfnI5ivkEGfq30fjmpOdBWBmII" width="350" />
                                        {/* <EmbeddedYoutube
                                            name='Demo'
                                            url={'https://www.youtube.com/watch?v=MXzv-XL6LLs'}
                                            width={700}
                                            height={480}
                                        /> */}
                                    </div>
                                }
                            />
                        </div>
                        {(yellowTriangle || redTriangle) && (
                            <ExtraInfo reminder={redTriangle ? 'Files are missing, both locally and in cloud storage. Your notebook will not be able to use them.' : 'Files are missing locally. Your notebook will be able to run with files in cloud storage but we will not be able to sync them with local copies.'}>
                                <WarningRounded fontSize={'small'} style={{color: redTriangle ? this.props.theme.palette.error.main : this.props.theme.palette.warning.main, marginTop: '4px'}} />
                            </ExtraInfo>
                        )}
                        <span style={{
                            margin: 'auto 15px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.filesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {files.length > 0 && (files.length + ' upload' + (files.length > 1 ? 's' : ''))}{files.length > 0 && dataConnectors.length > 0 ? ', ' : ''}{dataConnectors.length > 0 && (dataConnectors.length + ' connector' + (dataConnectors.length > 1 ? 's' : ''))}
                        </span>
                        <IconButton
                            onClick={() => {
                                Global.filesAccordionExpanded = !Global.filesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            style={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.filesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <Files />
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordionSummary style={{cursor: 'default'}}>
                    <SubHeader title='Notifications' />
                    <span style={{
                        margin: 'auto 15px',
                        flexGrow: 1,
                        textAlign: 'end',
                        opacity: 0.5,
                        transitionDuration: '217ms',
                        whiteSpace: 'nowrap',
                        fontSize: '12px',
                        fontStyle: 'italic',
                    }}>
                        {(() => {
                            let numEnabled = 0
							const config = Global.metadata.getMetadata().config
                            if (!config.interactive) {
                                const notifications = config.notifications;
                                if (notifications.jobStartedSMSEnabled) numEnabled++;
                                if (notifications.jobFailedSMSEnabled || notifications.jobCompletedSMSEnabled) numEnabled++;
                                // TODO:JJ This currently does not refresh automatically when Global.user.notificationsEnabled changes, and I wasn't sure how to quickly do this.
                                if (Global.user.notificationsEnabled && numEnabled > 0) {
                                    return numEnabled + ' enabled'
                                }
                            }
                        })()}
                    </span>
                    <NotificationsPopup disabled={Global.metadata.getMetadata().config.interactive} openUserDialogTo={this.props.openUserDialogTo} />
                </StyledAccordionSummary>
            </div>
        )
    }

	private handleLabShellChange = () => {this.forceUpdate()}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
        Global.user.fileChecker.start();
		Global.labShell.currentChanged.connect(this.handleLabShellChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.user.fileChecker.stop();
        Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
        this._isMounted = false
    }
    
    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
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
const ThemedFilesPanel = withTheme(FilesPanel)
export { ThemedFilesPanel as FilesPanel }