/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'

import { Button, OutlinedInput, Radio, Theme, withStyles, withTheme } from '@material-ui/core';
import { CSSProperties } from '@material-ui/styles';
import { Global } from '../../Global';
import { Dropdown } from '../../core';

enum Platform {
    LAPTOP = "laptop",
    COLAB = "colab",
    KAGGLE = "kaggle",
}

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

enum KaggleAccelerator {
    GPU = "GPU Accelerator",
    TPU = "TPU Accelerator",
    NONE = "No accelerator"
}

interface IProps {
    style?: CSSProperties
    theme: Theme
}

interface IState {
    runPlatform: string | null
    kaggleAccelerator: KaggleAccelerator | null
}

class WhereAreYouRunning extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super(props)
        this.state = {
            runPlatform: null,
            kaggleAccelerator: null,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                {/* This is the preview */}
                {this.state.runPlatform !== null && (
                    <>
                        {Global.capitalizeFirstLetter(this.state.runPlatform)}
                        {this.state.runPlatform === Platform.KAGGLE && (
                            <>
                                {': ' + this.state.kaggleAccelerator}
                            </>
                        )}
                    </>
                )}

                {/* This is the content */}
                <div style={{width: '100%', display: 'inline-flex'}}>
                    <Radio style={{padding: '3px'}} color='primary' checked={this.state.runPlatform === Platform.LAPTOP} onChange={() => this.safeSetState({ runPlatform: Platform.LAPTOP })}/>
                    <div style={{margin: 'auto 0px'}}>
                        {Global.capitalizeFirstLetter(Platform.LAPTOP)}
                    </div>
                </div>
                <div style={{width: '100%', display: 'inline-flex'}}>
                    <Radio style={{padding: '3px'}} color='primary' checked={this.state.runPlatform === Platform.COLAB} onChange={() => this.safeSetState({ runPlatform: Platform.COLAB })}/>
                    <div style={{margin: 'auto 0px'}}>
                        {Global.capitalizeFirstLetter(Platform.COLAB)}
                    </div>
                </div>
                <div style={{width: '100%', display: 'inline-flex'}}>
                    <Radio style={{padding: '3px'}} color='primary' checked={this.state.runPlatform === Platform.KAGGLE} onChange={() => this.safeSetState({ runPlatform: Platform.KAGGLE })}/>
                    <div style={{margin: 'auto 0px'}}>
                        {Global.capitalizeFirstLetter(Platform.KAGGLE)}
                    </div>
                    {this.state.runPlatform === Platform.KAGGLE && (
                        <Dropdown
                            style={{padding: '3px 0px'}}
                            getValue={() => this.state.kaggleAccelerator === null ? "Pick accelerator" : this.state.kaggleAccelerator }
                            saveValue={(value: string) => this.safeSetState({ kaggleAccelerator: value })}
                            values={["Pick accelerator", KaggleAccelerator.NONE, KaggleAccelerator.GPU, KaggleAccelerator.TPU].map(x => { return { value: x, description: '', disabled: x === "Pick accelerator"} })}
                        />
                    )}
                </div>
                <div style={{width: '100%', display: 'inline-flex'}}>
                    <Radio style={{padding: '3px'}} color='primary' checked={this.state.runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(this.state.runPlatform)} onChange={() => this.safeSetState({ runPlatform: "" })}/>
                    <div style={{margin: 'auto 0px'}}>
                        Other
                    </div>
                    {this.state.runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(this.state.runPlatform) && (
                        <StyledOutlinedInput
                            placeholder={'ex. AWS instance'}
                            style={{ margin: 'auto 6px' }}
                            value={this.state.runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(this.state.runPlatform) ? this.state.runPlatform : ''}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.safeSetState({ runPlatform : event.target.value })}
                        />
                    )}
                </div>
                
                <div style={{display: 'inline-flex'}}>
                    <Button
                        // onClick={() => this.safeSetState({ activeStep: 0 })}
                        style={{margin: '6px'}}
                    >
                        Back
                    </Button>
                    <Button
                        variant="contained"
                        color="primary"
                        // onClick={() => this.safeSetState({ activeStep: 2 })}
                        style={{margin: '6px'}}
                        disabled={this.state.runPlatform === null || this.state.runPlatform == '' || (this.state.runPlatform === Platform.KAGGLE && this.state.kaggleAccelerator === null)}
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
const ThemedWhereAreYouRunning = withTheme(WhereAreYouRunning)
export {ThemedWhereAreYouRunning as WhereAreYouRunning}
