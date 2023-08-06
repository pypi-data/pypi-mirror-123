/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { CSSProperties } from '@material-ui/styles'
import * as React from 'react'
// import { Tag } from '../../components/Tag'
import FormatUtils from '../../utils/FormatUtils'
import { Machine } from './Machine'

interface IProps {
    machine: Machine
    style?: CSSProperties
}
interface IState {}

export class MachinePreviewComponent extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        const machine = this.props.machine
        return (
            <div style={Object.assign({margin: '6px'}, this.props.style)}>
                {machine.getIdentityComponent()}
                <div style={{
                    display: 'inline-flex',
                    flexWrap: 'wrap',
                    width: '100%',
                    margin: '3px 0px',
                    fontSize: 'var(--jp-ui-font-size1)',
                }}>
                    <div style={{flexGrow: 1, margin: '3px 0px'}}>
                        Machine
                        {machine.getStateMessage() != '' && (
                            <>
                                {' (' + machine.getStateMessage() + ')'}
                            </>
                        )}
                        :
                    </div>
                    <div style={{display: 'inline-block', minWidth: '57px', margin: '3px 0px', textAlign: 'right'}}>
                        {machine.rate !== undefined && (machine.promo ? 'promo ' : '')}
                        <span style={{fontWeight: 'bold'}}>
                            {machine.rate !== undefined ? (FormatUtils.styleRateUnitValue()(machine.rate)) : 'No matches found'}
                        </span>
                    </div>
                </div>
            </div>
        )
    }
}