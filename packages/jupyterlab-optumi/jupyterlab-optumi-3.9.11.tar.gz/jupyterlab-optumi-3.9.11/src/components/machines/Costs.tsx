/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { Divider, Theme, withTheme } from '@material-ui/core';
import moment from 'moment';

import { WarningRounded } from '@material-ui/icons';
import { BillingType } from '../../models/User';

interface IProps {
    style?: React.CSSProperties
    rate: number,
    cost: number,
    balance: number,
    theme: Theme,
}

interface IState {}

function ordinal_suffix_of(i: number) {
    var j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
}

class Costs extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <div style={{display: 'flex', margin: '6px'}}>
                    <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '16px', lineHeight: '30px', fontWeight: 'bold'}}>
                        Rate
                    </div>
                    <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '14px', lineHeight: '30px', textAlign: 'right'}}>
                        <div>
                            ${this.props.rate.toFixed(2)}/hr
                        </div>
                    </div>
                </div>
                <Divider variant='middle' />
                {Global.user.billingType == BillingType.CREDIT_BUCKET || this.props.balance < 0 ? (
                    <>
                        <div style={{display: 'flex', margin: '6px'}}>
                            <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '16px', lineHeight: '30px', fontWeight: 'bold'}}>
                                Credits
                            </div>
                            <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '14px', lineHeight: '30px', textAlign: 'right'}}>
                                <div>
                                    Left: ${(-this.props.balance).toFixed(2)} 
                                </div>
                                {Global.user.billingType == BillingType.CREDIT_BUCKET && (
                                    <div>
                                        Used: ${this.props.cost.toFixed(2)}
                                    </div>
                                )}
                            </div>
                        </div>
                        <Divider variant='middle' />
                        {Global.user.billingType == BillingType.CREDIT_BUCKET && this.props.rate > 0 && (
                            (() => {
                                const dur = moment.duration(-this.props.balance / this.props.rate, 'hours');
                                var content: JSX.Element = null
                                if (dur.asHours() <= 2) {
                                    content = <WarningRounded style={{color: this.props.theme.palette.error.main, lineHeight: '20px', width: '20px', height: '20px', marginRight: '6px'}} />
                                } else if (dur.asHours() < 25) {
                                    content = <WarningRounded style={{color: this.props.theme.palette.warning.main, lineHeight: '20px', width: '20px', height: '20px', marginRight: '6px'}} />
                                }
                                return (
                                    <div style={{margin: '12px', justifyContent: 'center', height: '21px', display: 'inline-flex', width: 'calc(100% - 24px)'}}>
                                        <div style={{marginLeft: '-26px'}}>
                                            {content}
                                        </div>
                                        <div style={{lineHeight: '21px'}}>
                                            {dur.humanize()} left at current spending rate
                                        </div>
                                    </div>
                                )
                            })()
                        )}
                    </>
                ) : (
                    <>
                        <div style={{display: 'flex', margin: '6px'}}>
                            <div style={{flexGrow: 1, display: 'inline-flex'}}>
                                <div style={{justifyContent: 'center', fontSize: '16px', lineHeight: '30px', fontWeight: 'bold'}}>
                                    Usage
                                </div>
                                {Global.user.subscriptionActive && (
                                    <div style={{opacity: 0.5, margin: 'auto 6px'}}>
                                        Cycle resets on the {ordinal_suffix_of(Global.user.billingCycleAnchor.getDate())}
                                    </div>
                                )}
                            </div>
                            <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '14px', lineHeight: '30px', textAlign: 'right'}}>
                                <div>
                                    ${(this.props.balance).toFixed(2)}
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </>
        )
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

const ThemedCosts = withTheme(Costs)
export {ThemedCosts as Costs}