/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../../Global'
import Step from '../../core/Step';
import { PhoneNumberFormat, PhoneNumberUtil } from 'google-libphonenumber';
import { Button, Radio } from '@material-ui/core';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { StepperCallbacks } from '../../core/Stepper';

interface IProps {
    step: number
    stepperCallbacks: StepperCallbacks
}

export default function HowToNotifyStep(props: any) {
    const {step, stepperCallbacks} = props as IProps
    const optumi = Global.metadata.getMetadata().config;
    const phoneUtil = PhoneNumberUtil.getInstance();

    const savePackageReadySMSEnabledValue = (value: boolean): void => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        optumi.config.notifications.packageReadySMSEnabled = value;
        tracker.setMetadata(optumi);
    }

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return (
        <Step {...props}
            header={`How would you like to be notified when it's done?`}
            preview={() => {
                if (optumi.package.runPlatform !== null) {
                    // if (optumi.notifyVia === NotifyVia.EMAIL) {
                    //     return `Email: ${optumi.email}`
                    // } else {
                        if (optumi.notifications.packageReadySMSEnabled) {
                            return `Text: ${phoneUtil.format(phoneUtil.parse(Global.user.phoneNumber, 'US'), PhoneNumberFormat.INTERNATIONAL)}`
                        } else {
                            return `Don't notify me`
                        }
                    // }
                }
            }}
            overrideNextButton={
                <Button
                    onClick={() => stepperCallbacks.completeAndIncrement(step)}
                    style={{margin: '6px'}}
                    variant='contained'
                    color='primary'
                >
                    Next
                </Button>
            }
        >
            {/* <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={optumi.notifyVia === NotifyVia.EMAIL}
                    onChange={() => this.saveNotifyViaValue(NotifyVia.EMAIL)}
                />
                <div style={{margin: 'auto 0px'}}>
                    Email
                </div>
            </div>
            {optumi.notifyVia === NotifyVia.EMAIL && (
                <StyledOutlinedInput
                    placeholder={'example@gmail.com'}
                    fullWidth
                    value={optumi.email}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.saveEmailValue(event.target.value)}
                />
            )} */}
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={optumi.notifications.packageReadySMSEnabled}
                    onChange={() => savePackageReadySMSEnabledValue(true)}
                />
                <div style={{margin: 'auto 0px'}}>
                    {'Text to ' + phoneUtil.format(phoneUtil.parse(Global.user.phoneNumber, 'US'), PhoneNumberFormat.INTERNATIONAL)}
                </div>
            </div>
            {/* {optumi.notifications.packageReadySMSEnabled && (
                <PhoneTextBox
                    getValue={() => Global.user.phoneNumber}
                    saveValue={(phoneNumber: string) => {
                        if (phoneNumber == '') Global.user.notificationsEnabled = false;
                        // We will automatically turn on notification if the user enters their phone number
                        if (phoneNumber != '') Global.user.notificationsEnabled = true;
                        Global.user.phoneNumber = phoneNumber;
                        // We need to update so the button below will be updated properly
                        this.setState({ buttonKey: this.state.buttonKey+1 });
                    }}
                />
            )} */}
            <div style={{width: '100%', display: 'inline-flex'}}>
                <Radio
                    style={{padding: '3px'}}
                    color='primary'
                    checked={!optumi.notifications.packageReadySMSEnabled}
                    onChange={() => savePackageReadySMSEnabledValue(false)}
                />
                <div style={{margin: 'auto 0px'}}>
                    Don't notify me
                </div>
            </div>
        </Step>
    )
}