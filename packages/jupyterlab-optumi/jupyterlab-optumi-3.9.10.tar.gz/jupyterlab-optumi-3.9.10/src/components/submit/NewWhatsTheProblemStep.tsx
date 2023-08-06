/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { StepperCallbacks } from '../../core/Stepper';
import { Global } from '../../Global'
import Step, { StepOutlinedInput } from '../../core/Step';
import { InputAdornment, Radio } from '@material-ui/core';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';

interface IProps {
    step: number
    stepperCallbacks: StepperCallbacks
}

export default function WhatsTheProblemStep(props: any) {
    const {step, stepperCallbacks} = props as IProps
    const pack = Global.metadata.getMetadata().config.package;
    const [notebookRuns, setNotebookRuns] = React.useState<boolean>(pack.notebookRuns)
    const [runHours, setRunHours] = React.useState<number>(pack.runHours)
    const [runMinutes, setRunMinutes] = React.useState<number>(pack.runMinutes)

    React.useEffect(() => {
        const complete = notebookRuns === false || runHours !== 0 || runMinutes !== 0
        stepperCallbacks.setStepComplete(step, complete)
        if (complete) stepperCallbacks.incrementFocusMax(step)
    }, [notebookRuns, runHours, runMinutes])

    React.useEffect(() => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        optumi.config.package.notebookRuns = notebookRuns
        tracker.setMetadata(optumi);
    }, [notebookRuns])

    React.useEffect(() => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        optumi.config.package.runHours = runHours
        tracker.setMetadata(optumi);
    }, [runHours])

    React.useEffect(() => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        optumi.config.package.runMinutes = runMinutes
        tracker.setMetadata(optumi);
    }, [runMinutes])

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return (
        <Step {...props}
            header={`What's the problem with your notebook?`}
            preview={() => {
                if (notebookRuns === true) {
                    return `It runs too slow: ${runHours}h${runMinutes}m`
                } else if (notebookRuns === false) {
                    return `It doesn't run at all`
                }
            }}
        >
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={notebookRuns === false}
                    onChange={() => {
                        setNotebookRuns(false)
                    }}
                />
                <div style={{margin: 'auto 0px'}}>
                    It does not run at all
                </div>
            </div>
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={notebookRuns === true}
                    onChange={() => {
                        setNotebookRuns(true)
                    }}
                />
                <div style={{margin: 'auto 0px'}}>
                    It runs too slow
                </div>
            </div>
            {notebookRuns && (
                <div style={{display: 'inline-flex'}}>
                    <StepOutlinedInput
                        style={{width: '75px'}}
                        value={runHours}
                        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                            setRunHours(+event.target.value.replace(/\D/g,''))
                        }}
                        endAdornment={
                            <InputAdornment position='end' style={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                <span style={{fontSize: '12px'}}>
                                    hours
                                </span>
                            </InputAdornment>
                        }                                
                    />
                    <StepOutlinedInput
                        style={{width: '75px'}}
                        value={runMinutes}
                        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                            setRunMinutes(+event.target.value.replace(/\D/g,''))
                        }}
                        endAdornment={
                            <InputAdornment position='end' style={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                <span style={{fontSize: '12px'}}>
                                    minutes
                                </span>
                            </InputAdornment>
                        }
                    />
                </div>
            )}
        </Step>
    )
}