/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import {
    loadStripe,
	Stripe,
    StripeError,
} from '@stripe/stripe-js';
import { Button, CircularProgress } from '@material-ui/core';


// Properties from parent
interface IProps {}

// Properties for this component
interface IState {
    checkoutWaiting: boolean,
    portalWaiting: boolean,
}

const stripePromise = loadStripe(Global.stripe_key);

export class MeteredBillingCheckoutForm extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            checkoutWaiting: false,
            portalWaiting: false,
        }
    }

    private handleCheckoutClick = async () => {
        // Get Stripe.js instance    
        // Call your backend to create the Checkout Session
        
        this.safeSetState({ checkoutWaiting: true });

        const stripe: Stripe = await stripePromise;
        
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/create-checkout";
        const init: RequestInit = {
            method: 'POST',
            body: JSON.stringify({
                items: [],
                redirect: settings.baseUrl,
            }),
        };
        ServerConnection.makeRequest(
            url,
            init,
            settings
        ).then((response: Response) => {
            Global.handleResponse(response);
            return response.json();
        }).then((body: any) => {
            // When the customer clicks on the button, redirect them to Checkout.
            return stripe.redirectToCheckout({
                sessionId: body.id,
            });
        }).then((result: {error: StripeError}) => {
            this.safeSetState({ checkoutWaiting: false });
            if (result.error) {
                // If `redirectToCheckout` fails due to a browser or network
                // error, display the localized error message to your customer
                // using `result.error.message`.
            }
        });
    };

    private handlePortalClick = async () => {
        this.safeSetState({ portalWaiting: true });
        
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/create-portal";
        const init: RequestInit = {
            method: 'POST',
            body: JSON.stringify({
                redirect: settings.baseUrl,
            }),
        };
        ServerConnection.makeRequest(
            url,
            init,
            settings
        ).then((response: Response) => {
            Global.handleResponse(response);
            return response.json();
        }).then((body: any) => {
            // When the customer clicks on the button, redirect them to the portal
            window.location.href = body.url;
            this.safeSetState({ portalWaiting: false });
        });
    };

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                {Global.user.subscriptionActive ? (
                    <>
                        <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                            <div 
                                style={{
                                lineHeight: '24px',
                                margin: '0px 12px',
                                flexGrow: 1,
                            }}
                            >
                                {'You are subscribed to Optumi. To manage your subscription and other payment information, click the button below.'}
                            </div>
                        </div>
                        <div style={{padding: '6px', width: '100%'}}>
                            <Button 
                                disabled={this.state.portalWaiting} 
                                variant="contained"
                                style={{width: '100%'}}
                                onClick={this.handlePortalClick}
                            >
                                {this.state.portalWaiting ? (<CircularProgress size='1.75em'/>) : 'Payment Settings'}
                            </Button>
                        </div>
                    </>
                ) : (
                    <>
                        <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                            <div 
                                style={{
                                lineHeight: '24px',
                                margin: '0px 12px',
                                flexGrow: 1,
                            }}
                            >
                                {'Subscribe to use Optumi. You will be changed monthly for the virtual machines that you use.'}
                            </div>
                        </div>
                        <div style={{padding: '6px', width: '100%'}}>
                            <Button 
                                disabled={this.state.checkoutWaiting} 
                                color="primary" 
                                variant="contained"
                                style={{width: '100%'}}
                                onClick={this.handleCheckoutClick}
                            >
                                {this.state.checkoutWaiting ? (<CircularProgress size='1.75em'/>) : 'Subscribe'}
                            </Button>
                        </div>
                    </>
                )}
            </>
		);
    }
    
    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
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
}