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
import { Radio } from '@material-ui/core';
import { Dropdown } from '../../core';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { KaggleAccelerator, Platform } from '../../models/PackageConfig';

interface IProps {
    step: number
    stepperCallbacks: StepperCallbacks
}

export default function WheresItRunningStep(props: any) {
    const {step, stepperCallbacks} = props as IProps
    const pack = Global.metadata.getMetadata().config.package;
    const [runPlatform, setRunPlatform] = React.useState<string>(pack.runPlatform)
    const [kaggleAccelerator, setKaggleAccelerator] = React.useState<string>(pack.kaggleAccelerator)

    React.useEffect(() => {
        const complete = runPlatform === Platform.KAGGLE ? (
            kaggleAccelerator !== null
        ) : (
            runPlatform !== null && runPlatform !== ''
        )
        stepperCallbacks.setStepComplete(step, complete)
        if (complete) stepperCallbacks.incrementFocusMax(step)
    }, [runPlatform, kaggleAccelerator])



    React.useEffect(() => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        optumi.config.package.runPlatform = runPlatform
        tracker.setMetadata(optumi);
    }, [runPlatform])

    React.useEffect(() => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        optumi.config.package.kaggleAccelerator = kaggleAccelerator as KaggleAccelerator
        tracker.setMetadata(optumi);
    }, [kaggleAccelerator])

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return (
        <Step {...props}
            header={`Where are you currently running it?`}
            preview={() => {
                if (runPlatform !== null && runPlatform !== '') {
                    return Global.capitalizeFirstLetter(runPlatform) + (runPlatform === Platform.KAGGLE ? `: ${kaggleAccelerator === null ? 'Pick accelerator' : kaggleAccelerator}` : '')
                }
            }}
        >
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={runPlatform === Platform.LAPTOP}
                    onChange={() => setRunPlatform(Platform.LAPTOP)}
                />
                <div style={{margin: 'auto 0px'}}>
                    {Global.capitalizeFirstLetter(Platform.LAPTOP)}
                </div>
            </div>
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={runPlatform === Platform.COLAB}
                    onChange={() => setRunPlatform(Platform.COLAB)}
                />
                <div style={{margin: 'auto 0px'}}>
                    {Global.capitalizeFirstLetter(Platform.COLAB)}
                </div>
            </div>
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={runPlatform === Platform.KAGGLE}
                    onChange={() => setRunPlatform(Platform.KAGGLE)}
                />
                <div style={{margin: 'auto 0px'}}>
                    {Global.capitalizeFirstLetter(Platform.KAGGLE)}
                </div>
                {runPlatform === Platform.KAGGLE && (
                    <Dropdown
                        style={{padding: '3px 0px'}}
                        getValue={() => kaggleAccelerator === null ? 'Pick accelerator' : kaggleAccelerator }
                        saveValue={(value: string) => setKaggleAccelerator(value)}
                        values={['Pick accelerator', KaggleAccelerator.NONE, KaggleAccelerator.GPU, KaggleAccelerator.TPU].map(x => ({value: x, description: '', disabled: x === 'Pick accelerator'}))}
                    />
                )}
            </div>
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(runPlatform)}
                    onChange={() => setRunPlatform('')}
                />
                <div style={{margin: 'auto 0px'}}>
                    Other
                </div>
                {runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(runPlatform) && (
                    <StepOutlinedInput
                        placeholder={'ex. AWS instance'}
                        style={{ margin: 'auto 6px' }}
                        value={runPlatform !== '' && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(runPlatform) ? runPlatform : ''}
                        onChange={(event: React.ChangeEvent<HTMLInputElement>) => setRunPlatform(event.target.value)}
                    />
                )}
            </div>
        </Step>
    )
}