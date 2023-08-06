/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'

import { Button, InputAdornment, OutlinedInput, Radio, Theme, withStyles, withTheme } from '@material-ui/core';
import { CSSProperties } from '@material-ui/styles';
import { Global } from '../../Global';

const StyledOutlinedInput = withStyles({
    root: {
        padding: '0px',
        margin: '0px 3px',
        height: '21px',
    },
    input: {
        fontSize: '12px',
        padding: '3px 6px 3px 6px',
    },
    adornedEnd: {
        paddingRight: '0px',
    },
}) (OutlinedInput)


interface IProps {
    style?: CSSProperties
    theme: Theme
}

interface IState {
    notebookRuns: true | false | null,
    runHours: number,
    runMinutes: number,
}

class DoesYourNotebookRun extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super(props)
        this.state = {
            notebookRuns: null,
            runHours: 0,
            runMinutes: 0,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                {/* This is the preview */}
                {this.state.notebookRuns === true && (
                    <>
                        {'It runs too slow: ' + this.state.runHours + 'h' + this.state.runMinutes + 'm'}
                    </>
                )}
                {this.state.notebookRuns === false && (
                    <>
                        It doesn't run at all
                    </>
                )}

                {/* This is the content */}
                <div style={{width: '100%', display: 'inline-flex'}}>
                    <Radio style={{padding: '3px'}} color='primary' checked={this.state.notebookRuns === false} onChange={() => this.safeSetState({ notebookRuns: false })}/>
                    <div style={{margin: 'auto 0px'}}>
                        It does not run at all
                    </div>
                </div>
                <div style={{width: '100%', display: 'inline-flex'}}>
                    <Radio style={{padding: '3px'}} color='primary' checked={this.state.notebookRuns === true} onChange={() => this.safeSetState({ notebookRuns: true })}/>
                    <div style={{margin: 'auto 0px'}}>
                        It runs too slow
                    </div>
                </div>
                {this.state.notebookRuns && (
                    <div style={{display: 'inline-flex'}}>
                        <StyledOutlinedInput
                            style={{width: '75px'}}
                            value={this.state.runHours}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.safeSetState({ runHours : +(event.target.value.replace(/\D/g,''))})}
                            endAdornment={
                                <InputAdornment position="end" style={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                    <span style={{fontSize: '12px'}}>
                                        hours
                                    </span>
                                </InputAdornment>
                            }                                
                        />
                        <StyledOutlinedInput
                            style={{width: '75px'}}
                            value={this.state.runMinutes}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.safeSetState({ runMinutes : +(event.target.value.replace(/\D/g,''))})}
                            endAdornment={
                                <InputAdornment position="end" style={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                    <span style={{fontSize: '12px'}}>
                                        minutes
                                    </span>
                                </InputAdornment>
                            }
                        />
                    </div>
                )}
                <div style={{display: 'inline-flex'}}>
                    <Button
                        // onClick={() => this.safeSetState({ activeStep: -1 })}
                        style={{margin: '6px'}}
                    >
                        Back
                    </Button>
                    <Button
                        variant="contained"
                        color="primary"
                        // onClick={() => this.safeSetState({ activeStep: 1 })}
                        style={{margin: '6px'}}
                        disabled={this.state.notebookRuns === null || (this.state.notebookRuns && this.state.runHours === 0 && this.state.runMinutes === 0)}
                    >
                        Next
                    </Button>
                </div>
            </>
		);
	}

    private handleThemeChange = () => this.forceUpdate()
    private handleMetadataChange = () => this.forceUpdate()

    public componentDidMount = () => {
		this._isMounted = true;
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
		this._isMounted = false;
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
const ThemedDoesYourNotebookRun = withTheme(DoesYourNotebookRun)
export {ThemedDoesYourNotebookRun as DoesYourNotebookRun}
