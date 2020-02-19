// Copyright (c) cccs-is
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

import {
  ServerConnection
} from '@jupyterlab/services';

// import {
//   showErrorMessage
// } from '@jupyterlab/apputils';



// Import the CSS
import '../css/widget.css'


export
class AuthModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: AuthModel.model_name,
      _model_module: AuthModel.model_module,
      _model_module_version: AuthModel.model_module_version,
      _view_name: AuthModel.view_name,
      _view_module: AuthModel.view_module,
      _view_module_version: AuthModel.view_module_version,
      value : 'Hello World'
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  public authenticate() {
    console.log('Authenticate() ->')
  }

  static model_name = 'AuthModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'AuthView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}


export
class AuthView extends DOMWidgetView {

  //_serverSettings: ServerConnection.ISettings;
   _serverSettings = ServerConnection.makeSettings();

  // constructor() {
  //   super();
  //   // this._serverSettings = ServerConnection.makeSettings();
  // }

  public initialize(opts: any) {
    super.initialize(opts);
    this.render();
    
  }

  public render() {
    this.el.classList.add('custom-widget');
    this.$el.html(`<button id='auth-button'> Get Token </button>`);

    // this.value_changed();
    //this.model.on('change:value', this.value_changed, this);
  }

  public events() {
    // return {
    //   'click #auth-button': () => this.send({event: 'click:button'})
    // }
    return {
      'click #auth-button': () => {this.getTokens()}
    }
  }

  //const buildWindowProps = objProps => {
  //  const strProps = Object.entries(objProps)
  //      .map(e => `${e[0]} = ${e[1]}`)
  //      .join(',');
  //  return strProps;
  //}

  public getTokens() {
    console.log('Getting Tokens()')
    console.log('>> ', this._serverSettings.baseUrl + 'pymango/authenticate')
    //this._sendRequest()

    //let props = {
    //        menubar: 'yes',
    //        location: 'no',
    //        resizable: 'yes',
    //        scrollbars: 'yes',
    //        status: 'yes',
    //        width: '660',
    //        height: '790',
    //};

    //let strProps = Object.entries(props).map(e => `${e[0]} = ${e[1]}`).join(',');
    //let strProps = Array.from(props.entries()).forEach(e => `${e[0]} = ${e[1]}`).join(',')
    //props = buildWindowProps(strProps)
    let strProps = "menubar='yes', location='no', resizable='yes', scrollbar='yes', status='yes', width='400', height='600'" 
    let auth_url = " https://login.microsoftonline.com/fa9b7bc4-84f2-4ea2-932a-26ca2f5fb014/oauth2/v2.0/authorize?client_id=b989b926-a638-488f-b6c9-02d4a0289c14&response_type=code&redirect_uri=https%3A%2F%2Fjupyhub.exp.pilot.aadtest.ca%2Fuser-redirect%2Fpymango%2Fcallback&scope=offline_access+openid+profile&state=1f3bbe10-2d73-4b16-9b67-42da340b79d0"
   // window.location.href = redirect_url
    let x = window.open(auth_url, "MY AUTH", strProps)
    console.log("done getTokens()", x)
  }
//  private async _sendRequest() : Promise<void> {
//    // throw new Error("Method not implemented.");
//    const response = await ServerConnection.makeRequest(
//      `${this._serverSettings.baseUrl}pymango/authenticate`,
//      { method: 'GET' },
//      this._serverSettings
//    );
//
//    // if (response.status != 200) {
//    //   const err = await response.json();
//    //   void showErrorMessage('Failed to authenticate and obtain tokens', err);
//    //   throw err;
//    // }
//    console.log(response)
//    console.log(' we need to send the requst to get the tokens')
//    console.log(' TBD....')
//    return response.json();
//  }

  
}
