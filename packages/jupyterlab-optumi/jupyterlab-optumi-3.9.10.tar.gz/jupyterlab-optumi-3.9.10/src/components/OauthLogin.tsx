///<reference path="../../node_modules/@types/node/index.d.ts"/>

/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { User } from '../models/User';

import {
	Container,
	Button,
	TextField,
	Link,
	Typography,
	CircularProgress,
	withStyles,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
	InputAdornment,
 } from '@material-ui/core';

 import ArrowForwardIcon from '@material-ui/icons/ArrowForward';

import { ServerConnection } from '@jupyterlab/services';
import { Header, ShadowedDivider } from '../core';

// Element to display the Copyright with optumi.com link
function Copyright() {
	return (
		<Typography style={{marginBottom: '10px'}} variant="body2" color="textSecondary" align="center">
			{'Copyright © '}
			<Link color="inherit" href="https://optumi.com/">
				Optumi Inc
			</Link>
		</Typography>
	);
}

const StyledDialog = withStyles({
    root: {
        margin: '12px',
        padding: '0px',
    },
    paper: {
        backgroundColor: 'var(--jp-layout-color1)',
    },
})(Dialog)

// Properties from parent
interface IProps {}

// Properties for this component
interface IState {
	domain: string;
	loginFailed: boolean;
	domainFailed: boolean;
	loginFailedMessage: string;
	waiting: boolean;
	spinning: boolean;
	packageString: string;
	downgrade: boolean;
}

// The login screen
export class OauthLogin extends React.Component<IProps, IState> {
	_isMounted = false;

	constructor(props: IProps) {
		super(props);
		this.state = {
			domain: Global.domain,
			loginFailed: false,
            domainFailed: false,
            loginFailedMessage: "",
			waiting: false,
			spinning: false,
			packageString: "",
			downgrade: false,
		}
	}

	private handleDomainChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (new RegExp('^[A-Za-z0-9.:]*$').test(value)) {
            this.safeSetState({domain: value, loginFailed: false, domainFailed: false});
        }
	}

	private handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
		if (e.key === 'Enter') {
			this.login();
		}
	}

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                <div className='jp-optumi-logo'/>				

                <Container style={{textAlign: 'center'}} maxWidth="xs">
                    <form>
						<div style={{display: 'inline-flex'}}>
							<TextField
								fullWidth
								required
								style={{marginTop: "16px", marginBottom: "8px"}}
								label="Domain"
								variant="outlined"
								value={this.state.domain}
								onChange = {this.handleDomainChange}
								onKeyDown = { this.handleKeyDown }
								error={ this.state.domainFailed }
								helperText={ this.state.domainFailed? "Unable to contact " + this.state.domain : ""}
								InputProps={{
									endAdornment: <InputAdornment position="start">.optumi.net</InputAdornment>,
								}}
						
							/>
							<Button
								style={{marginLeft: '8px', marginTop: "16px", marginBottom: "8px", minWidth: '0px'}}
								variant="contained"
								color="primary"
								disabled={this.state.waiting}
								onClick={ () => this.login() }
							>
								{this.state.waiting && this.state.spinning ? <CircularProgress size='1.75em'/> : <ArrowForwardIcon />}
							</Button>
						</div>
                    </form>
                    <div style={{marginTop: "30px"}} />
                    <Copyright />
                    {/* <div dangerouslySetInnerHTML={{__html: this.fbWidget.node.innerHTML}} /> */}
                </Container>
				<StyledDialog
					onClose={(event: object, reason: string) => void 0}
					open={this.state.packageString != ""}
				>
					<DialogTitle
						disableTypography
						style={{
							backgroundColor: 'var(--jp-layout-color2)',
							height: '48px',
							padding: '6px 30px',
						}}
					>
						<Header
							title={this.state.downgrade ? "Switch to compatible JupyterLab extension" : "Upgrade JupyterLab extension"}
							style={{lineHeight: '24px'}}
						/>
					</DialogTitle>
					<ShadowedDivider />
					<div style={{padding: '18px'}}>
						<DialogContent style={{padding: '6px 18px', lineHeight: '24px'}}>
							<div>
								{this.state.downgrade ? 
									"Sorry, we've noticed an incompatibility between this JupyterLab extension version and our backend. To switch to a compatible JupyterLab extension run the command"
								:
									"We've made enhancements on the backend that require a new JupyterLab extension version. To upgrade your JupyterLab extension run the command"
								}
							</div>
							<textarea
								id="optumi-upgrade-string"
								style={{
									fontFamily: 'var(--jp-code-font-family)',
									width: '100%',
									lineHeight: '18px',
									marginTop: '6px',
								}}
								rows={1}
								readOnly
							>
								{'pip install ' + this.state.packageString}
							</textarea>
							<div>
								{'and restart JupyterLab.'}
							</div>
						</DialogContent>
						<DialogActions style={{padding: '12px 6px 6px 6px'}}>
							<Button
								variant='contained'
								onClick={() => {
									var copyTextarea: HTMLTextAreaElement = document.getElementById('optumi-upgrade-string') as HTMLTextAreaElement;
									copyTextarea.focus();
									copyTextarea.select();

									try {
										document.execCommand('copy');
									} catch (err) {
										console.log(err);
									}
								}}
								color={'primary'}
							>
								Copy command
							</Button>
							<Button
								variant='contained'
								onClick={() => {
									this.safeSetState({loginFailed: false, domainFailed: false, packageString: "", downgrade: false, loginFailedMessage: ""});
								}}
								color={'secondary'}
							>
								Close
							</Button>
						</DialogActions>
					</div>
				</StyledDialog>
        	</>
		);
	}

	// Try to log into the REST interface and update state according to response
	private async login() {
		this.safeSetState({ waiting: true, spinning: false });
		setTimeout(() => this.safeSetState({ spinning: true }), 1000);
		Global.domain = this.state.domain;
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/login";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				'domain': this.state.domain,
			})
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			this.safeSetState({ waiting: false })
			if (response.status !== 200 && response.status !== 201) {
                this.safeSetState({ loginFailed: false, domainFailed: true });
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		}, () => this.safeSetState({ waiting: false })).then((body: any) => {
            var newTab: Window = window.open(window.location.origin + '/optumi/oauth-login')
			this.checking_login = true;
            this.check_login(newTab)
			// if (body.loginFailed || body.domainFailed) {
			// 	if (body.message == 'Version exchange failed') {
			// 		var rawVersion = body.loginFailedMessage;
			// 		var split = rawVersion.split('-')[0].split('.');
			// 		const downgrade = Global.version.split('.')[1] > split[1];
			// 		var packageString = '"jupyterlab-optumi>=' + split[0] + '.' + split[1] + '.0,' + '<' + split[0] + '.' + (+split[1] + 1) + '.0"'
			// 		this.safeSetState({ loginFailed: body.loginFailed || false, domainFailed: body.domainFailed || false, packageString: packageString, downgrade: downgrade});
			// 	} else {
			// 		this.safeSetState({ loginFailed: body.loginFailed || false, domainFailed: body.domainFailed || false, loginFailedMessage: body.loginFailedMessage || ""});
			// 	}
			// } else {
			// 	var user = User.handleLogin(body);
			// 	Global.user = user;
			// 	this.safeSetState({ loginFailed: false, domainFailed: false });
			// }
		});
	}

	private checking_login = false;
    private async check_login(newTab: Window) {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/login";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (response.status !== 200 && response.status !== 201) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		}).then((body: any) => {
            if (body.domainFailed || body.loginFailed) {
				// No login yet, queue up another try
                if (this.checking_login) setTimeout(() => {
                    this.check_login(newTab);
                }, 1000);
			} else {
				this.checking_login = false;
				var user = User.handleLogin(body);
                newTab.close();
				Global.user = user;
			}
		});
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

	handleGlobalDomainChange = () => this.safeSetState({ domain: Global.domain });

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
        Global.onDomainChange.connect(this.handleGlobalDomainChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.onDomainChange.connect(this.handleGlobalDomainChange);
		this._isMounted = false;
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
