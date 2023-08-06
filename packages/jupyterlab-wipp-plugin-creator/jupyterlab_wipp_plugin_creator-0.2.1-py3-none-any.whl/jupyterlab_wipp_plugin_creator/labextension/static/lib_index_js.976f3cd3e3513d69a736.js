"use strict";
(self["webpackChunkjupyterlab_wipp_plugin_creator"] = self["webpackChunkjupyterlab_wipp_plugin_creator"] || []).push([["lib_index_js"],{

/***/ "./lib/addedFilesWidget.js":
/*!*********************************!*\
  !*** ./lib/addedFilesWidget.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AddedFilesWidget": () => (/* binding */ AddedFilesWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");


class AddedFilesWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(state) {
        super();
        this._addedFileNames = [];
        this._state = state;
        this._addedFileDiv = document.createElement('p');
        this.node.appendChild(this._addedFileDiv);
        let button = document.createElement('button');
        button.innerHTML = 'Update list of files';
        button.onclick = () => this.update();
        this.node.appendChild(button);
        this.update();
    }
    onUpdateRequest(msg) {
        this._state.fetch(_extensionConstants__WEBPACK_IMPORTED_MODULE_1__.ExtensionConstants.dbkey).then(response => {
            this._addedFileNames = response;
            let text = 'Added Files: <br>';
            if (this._addedFileNames) {
                for (let i = 0; i < this._addedFileNames.length; i++) {
                    text += this._addedFileNames[i] + "<br>";
                }
            }
            this._addedFileDiv.innerHTML = text;
        });
    }
    getValue() {
        return this._addedFileNames;
    }
}


/***/ }),

/***/ "./lib/extensionConstants.js":
/*!***********************************!*\
  !*** ./lib/extensionConstants.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ExtensionConstants": () => (/* binding */ ExtensionConstants)
/* harmony export */ });
class ExtensionConstants {
}
ExtensionConstants.dbkey = 'wipp-plugin-creator:data';


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab_wipp_plugin_creator', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./sidebar */ "./lib/sidebar.js");
/* harmony import */ var _style_logo_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/logo.svg */ "./style/logo.svg");







const logoIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
    name: 'wipp-plugin-builder:logo',
    svgstr: _style_logo_svg__WEBPACK_IMPORTED_MODULE_4__["default"]
});
let filepaths = [];
const plugin = {
    id: 'jupyterlab_wipp_plugin_creator:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__.IStateDB],
    activate: (app, factory, labShell, state) => {
        // Initialzie dbkey if not in IStateDB
        state.list().then(response => {
            let keys = response.ids;
            if (keys.indexOf(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey) === -1) {
                state.save(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey, filepaths);
            }
        });
        // Create the WIPP sidebar panel
        const sidebar = new _sidebar__WEBPACK_IMPORTED_MODULE_6__.CreatorSidebar(state);
        sidebar.id = 'wipp-labextension:plugin';
        sidebar.title.icon = logoIcon;
        sidebar.title.caption = 'WIPP Plugin Creator';
        labShell.add(sidebar, 'left', { rank: 200 });
        // Add context menu command, right click file browser to register marked files to be converted to plugin
        var filepath = '';
        const addFileToPluginContextMenuCommandID = 'wipp-plugin-creator-add-context-menu';
        app.commands.addCommand(addFileToPluginContextMenuCommandID, {
            label: 'Add to the new WIPP plugin',
            iconClass: 'jp-MaterialIcon jp-AddIcon',
            isVisible: () => ['notebook', 'file'].includes(factory.tracker.currentWidget.selectedItems().next().type),
            execute: () => {
                filepath = factory.tracker.currentWidget.selectedItems().next().path;
                state.fetch(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey).then(response => {
                    filepaths = response;
                    if (filepaths.indexOf(filepath) === -1) {
                        filepaths.push(filepath);
                    }
                    else {
                        console.log(`${filepath} was already added`);
                    }
                    state.save(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey, filepaths);
                });
            }
        });
        // Add command to context menu
        const selectorItem = '.jp-DirListing-item[data-isdir]';
        app.contextMenu.addItem({
            command: addFileToPluginContextMenuCommandID,
            selector: selectorItem
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CreatorSidebar": () => (/* binding */ CreatorSidebar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @deathbeds/jupyterlab-rjsf */ "webpack/sharing/consume/default/@deathbeds/jupyterlab-rjsf/@deathbeds/jupyterlab-rjsf");
/* harmony import */ var _deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _addedFilesWidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./addedFilesWidget */ "./lib/addedFilesWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _WippPluginSchema_json__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./WippPluginSchema.json */ "./lib/WippPluginSchema.json");





class CreatorSidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Create a new WIPP plugin creator sidebar.
     */
    constructor(state) {
        super();
        this.addClass('wipp-pluginCreatorSidebar');
        // Define Widget layout
        let layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        let title = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        let h1 = document.createElement('h1');
        h1.innerText = "Create New Plugin";
        title.node.appendChild(h1);
        layout.addWidget(title);
        //necessary or plugin will not activate
        const schema = _WippPluginSchema_json__WEBPACK_IMPORTED_MODULE_2__;
        this._addFileWidget = new _addedFilesWidget__WEBPACK_IMPORTED_MODULE_3__.AddedFilesWidget(state);
        layout.addWidget(this._addFileWidget);
        const formData = {
            name: "My Plugin",
            version: "0.1.0",
            requirements: [''],
            inputs: [{}],
            outputs: [{}],
        };
        this._form = new _deathbeds_jupyterlab_rjsf__WEBPACK_IMPORTED_MODULE_1__.SchemaForm(schema, { formData: formData });
        layout.addWidget(this._form);
        const runButtonWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const runButton = document.createElement('button');
        runButton.className = 'run';
        runButton.onclick = () => {
            this.submit();
        };
        runButton.innerText = "Create Plugin";
        runButtonWidget.node.appendChild(runButton);
        layout.addWidget(runButtonWidget);
    }
    //Sidebar constructor ends
    submit() {
        //Create API request on submit
        let formValue = this._form.getValue();
        let request = {
            formdata: formValue.formData,
            addedfilepaths: this._addFileWidget.getValue()
        };
        if (formValue.errors !== null) {
            var fullRequest = {
                method: 'POST',
                body: JSON.stringify(request)
            };
            (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('createplugin', fullRequest)
                .then(response => {
                console.log('POST request sent.');
            })
                .catch(() => console.log('There is an error making POST CreatePlugin API request.'));
        }
        else {
            console.log(`Schema form data returns with an error`);
            console.log(formValue.errors);
        }
    }
}


/***/ }),

/***/ "./style/logo.svg":
/*!************************!*\
  !*** ./style/logo.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"1792\" height=\"1792\" viewBox=\"0 0 1792 1792\" xmlns=\"http://www.w3.org/2000/svg\">\n    <path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M896 1629l640-349v-636l-640 233v752zm-64-865l698-254-698-254-698 254zm832-252v768q0 35-18 65t-49 47l-704 384q-28 16-61 16t-61-16l-704-384q-31-17-49-47t-18-65v-768q0-40 23-73t61-47l704-256q22-8 44-8t44 8l704 256q38 14 61 47t23 73z\"/>\n</svg> ");

/***/ }),

/***/ "./lib/WippPluginSchema.json":
/*!***********************************!*\
  !*** ./lib/WippPluginSchema.json ***!
  \***********************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Plugin Info","type":"object","properties":{"name":{"type":"string","title":"Name","default":""},"version":{"type":"string","title":"Version","default":""},"requirements":{"type":"array","items":{"type":"string"},"title":"Requirements"},"inputs":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string","title":"Name"},"description":{"type":"string","title":"Description"},"inputType":{"type":"string","enum":["collection","csvCollection","notebook","pyramid","genericData","stitchingVector"]},"required":{"type":"boolean","title":"Required"}}},"title":"Inputs"},"outputs":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string","title":"Name"},"description":{"type":"string","title":"Description"},"inputType":{"type":"string","enum":["collection","csvCollection","notebook","pyramid","genericData","stitchingVector"]},"required":{"type":"boolean","title":"Required"}}},"title":"Outputs"}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.976f3cd3e3513d69a736.js.map