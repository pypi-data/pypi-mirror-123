/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { StepperCallbacks } from '../../core/Stepper';
import { Global } from '../../Global'
import Step from '../../core/Step';
import { Button, createTheme, Dialog, DialogContent, DialogTitle, IconButton, MuiThemeProvider, useTheme, withStyles } from '@material-ui/core';
import FileServerUtils from '../../utils/FileServerUtils';
import { Header } from '../../core';
import CloseIcon from '@material-ui/icons/Close';
import { Package, PackageState } from '../../models/Package';
import { Machine, NoMachine } from '../../models/machine/Machine';
import { OptumiConfig } from '../../models/OptumiConfig';
import { ServerConnection } from '@jupyterlab/services';
import { createPatch } from 'diff';
import { html } from 'diff2html';

const StyledDialog = withStyles({
    paper: {
        width: '80%',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    step: number
    stepperCallbacks: StepperCallbacks
    openDeployPage: () => any
}

export default function AcceptChangesStep(props: any) {
    const {openDeployPage, ...NotOpenDeployPageProps} = props
    props = NotOpenDeployPageProps
    const {step, stepperCallbacks} = props as IProps
    const [open, setOpen] = React.useState<boolean>(false)
    const [pack, setPack] = React.useState<Package>(Global.metadata.getPackage())
    const [optimizedMachines, setOptimizedMachines] = React.useState<Machine[]>([])
    const [diffHTML, setDiffHTML] = React.useState<string>('')
    const theme = useTheme()
    const greenTheme = createTheme({ palette: { primary: theme.palette.success } })

    React.useEffect(() => { componentDidMount(); return componentWillUnmount }, [])

    const componentDidMount = (): void => {
        Global.metadata.getPackageChanged().connect(handleUpdate)
        Global.tracker.currentChanged.connect(handleUpdate)
    }

    const componentWillUnmount = (): void => {
        Global.metadata.getPackageChanged().disconnect(handleUpdate)
        Global.tracker.currentChanged.disconnect(handleUpdate)
    }

    const handleUpdate = (): void => {
        setPack(Global.metadata.getPackage())
        if (pack !== null && pack.packageState === PackageState.SHIPPED) {
            previewNotebook(pack.optimizedConfig).then(machines => setOptimizedMachines([machines[0]]))
            setDiffHTML(getDiff(pack.originalNotebook, pack.optimizedNotebook))
        }
    }

    const getDiff = (originalNotebook: any, optimizedNotebook: any): string => {
        try {
            // Convert to readable text
            var originalText = ""
            for (let cell of originalNotebook.cells) {
                if (cell.cell_type == 'code') {
                    originalText += cell.source
                }
                originalText += '\n'
            }

            var optimizedText = ""
            for (let cell of optimizedNotebook.cells) {
                if (cell.cell_type == 'code') {
                    optimizedText += cell.source
                }
                optimizedText += '\n'
            }

            if (originalText == optimizedText) return '<div style="padding: 6px;">No suggested notebook changes</div>'

            var diff = createPatch("notebook", originalText, optimizedText);
            return html(diff, { outputFormat: 'side-by-side', drawFileList: false });
        } catch (err) {
            console.warn(err)
        }
    }

    const previewNotebook = async (config: OptumiConfig): Promise<Machine[]> => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/preview-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbConfig: JSON.stringify(config),
                includeExisting: false,
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
            if (body.machines.length == 0) return [new NoMachine()]; // we have no recommendations
            const machines: Machine[] = [];
            for (let machine of body.machines) {
                machines.push(Object.setPrototypeOf(machine, Machine.prototype));
            }
			return machines;
		});
	}

    const formatOptimizedRuntime = (): string => {
        if (pack && pack.optimizedConfig) {
            const packConfig = pack.optimizedConfig.package;
            var ret = ''
            if (packConfig.runHours > 0) {
                ret += packConfig.runHours + ' hour'
                if (packConfig.runHours > 1) ret += 's'
                ret += ' '
            }
            ret += packConfig.runMinutes + ' minute'
            if (packConfig.runMinutes > 1) ret += 's'
            return ret
        }
    }

    const getOptimizedCost = (): string => {
        if (pack && pack.optimizedConfig) {
            const machine = optimizedMachines[0]
            const packConfig = pack.optimizedConfig.package;
            if (machine) return '$' + ((machine.rate * packConfig.runHours) + ((machine.rate / 60) * packConfig.runMinutes)).toFixed(2)
        }
    }

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return (
        <Step {...props}
            header={`Review and accept the changes`}
            overrideNextButton={
                <MuiThemeProvider theme={greenTheme}>
                    <Button
                        onClick={() => setOpen(true)}
                        disabled={stepperCallbacks.isStepDisabled(step + 1)}
                        style={{margin: '6px'}}
                        variant='contained'
                        color='primary'
                    >
                        View
                    </Button>
                </MuiThemeProvider>
            }
        >
            <StyledDialog
                open={open}
                onClose={() => setOpen(false)}
                scroll='paper'
            >
                <DialogTitle
                    disableTypography
                    style={{
                        display: 'inline-flex',
                        backgroundColor: 'var(--jp-layout-color2)',
                        height: '60px',
                        padding: '6px',
                        borderRadius: '4px',
                    }}
                >
                    <div style={{
                        display: 'inline-flex',
                        minWidth: '150px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                    }}>
                        <div style={{margin: '12px'}}>
                        Optimizations
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
                        <div style={{flexGrow: 1}} />
                        <Button
                            disableElevation
                            style={{
                                height: '36px',
                                margin: '6px',
                            }}
                            onClick={() => {
                                const pack = Global.metadata.getPackage();
                                Global.metadata.openPackage(true, true)

                                // Update the code
                                const current = Global.tracker.currentWidget;
                                current.content.model.fromJSON(pack.optimizedNotebook)

                                // Update the metadata
                                const metadata = Global.metadata.getMetadata();
                                metadata.config = pack.optimizedConfig;
                                Global.metadata.setMetadata(metadata);

                                setOpen(false)
                                stepperCallbacks.setStepSelected(step - 2)
                                stepperCallbacks.setFocusMax(step - 2)

                                openDeployPage()
                            }}
                            variant='contained'
                            color='primary'
                        >
                            Replace existing notebook
                        </Button>
                        <Button
                            disableElevation
                            style={{
                                height: '36px',
                                margin: '6px',
                            }}
                            onClick={async () => {
                                const pack = Global.metadata.getPackage();
                                Global.metadata.openPackage(true, true)

                                // Open the code in a new notebook
                                var path = Global.tracker.currentWidget.context.path;
                                
                                var inc = 0;
                                var newPath = path;
                                while ((await FileServerUtils.checkIfPathExists(newPath))[0]) {
                                    inc++;
                                    newPath = inc == 0 ? path : path.replace('.', '(' + inc + ').');
                                }

                                Global.metadata.setMetadataAfterOpen(newPath, pack.optimizedConfig);

                                FileServerUtils.saveNotebook(newPath, pack.optimizedNotebook).then((success: boolean) => {
                                    Global.docManager.open(newPath);
                                });

                                setOpen(false)
                                stepperCallbacks.setStepSelected(step - 2)
                                stepperCallbacks.setFocusMax(step - 2)

                                openDeployPage()
                            }}
                            variant='contained'
                            color='primary'
                        >
                            Open as a new notebook
                        </Button>
                    </div>
                    <IconButton
                        onClick={() => setOpen(false)}
                        style={{
                            display: 'inline-block',
                            width: '36px',
                            height: '36px',
                            padding: '3px',
                            margin: '6px',
                        }}
                    >
                        <CloseIcon
                            style={{
                                width: '30px',
                                height: '30px',
                                padding: '3px',
                            }}
                        />
                    </IconButton>
                </DialogTitle>
                <DialogContent style={{
                    flexGrow: 1, 
                    width: '100%',
                    height: '100%',
                    padding: '0px',
                    marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                    // lineHeight: 'var(--jp-code-line-height)',
                    fontSize: 'var(--jp-ui-font-size1)',
                    fontFamily: 'var(--jp-ui-font-family)',
                }}>
                    <div style={{height: '100%', overflow: 'auto', padding: '20px'}}>
                        <div style={{}}>
                            <Header title="Estimates" />
                            <div style={{margin: '6px'}}>Runtime: <span style={{fontWeight: 'bold'}}>{formatOptimizedRuntime()}</span></div>
                            <div style={{margin: '6px'}}>Cost: <span style={{fontWeight: 'bold'}}>{getOptimizedCost()}</span></div>
                        </div>
                        <div style={{display: 'inline-flex', width: '50%'}}>
                            {/* <div style={{flexGrow: 1}}>
                                <Header title="Original Resource Selection" />
                                {this.state.originalMachines.map(m => m.getPreviewComponent())}
                            </div> */}
                            <div style={{flexGrow: 1, paddingTop: '6px'}}>
                                <Header title="Resource Optimization" />
                                {optimizedMachines.map(m => m.getPreviewComponent())}
                            </div>
                        </div>
                        <div style={{flexGrow: 1, paddingTop: '6px'}}>
                            <Header title="Notebook Optimization" />
                            {/* position: relative is needed here otherwise the line numbers for the diff do not scroll with the rest of the page*/}
                            <div style={{position: 'relative'}} dangerouslySetInnerHTML={{ __html: diffHTML }} />
                        </div>
                    </div>
                </DialogContent>
            </StyledDialog>
        </Step>
    )
}