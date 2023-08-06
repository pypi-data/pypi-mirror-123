(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[1],{

/***/ 1181:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react-redux/es/index.js + 21 modules
var es = __webpack_require__(66);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react/index.js
var react = __webpack_require__(0);
var react_default = /*#__PURE__*/__webpack_require__.n(react);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/prop-types/index.js
var prop_types = __webpack_require__(1);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/classnames/index.js
var classnames = __webpack_require__(18);
var classnames_default = /*#__PURE__*/__webpack_require__.n(classnames);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/ui/src/index.js + 105 modules
var src = __webpack_require__(14);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/core/src/index.js + 33 modules
var core_src = __webpack_require__(17);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/core/src/DICOMSR/index.js + 8 modules
var DICOMSR = __webpack_require__(288);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/core/src/extensions/MODULE_TYPES.js
var MODULE_TYPES = __webpack_require__(689);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/moment/moment.js
var moment = __webpack_require__(7);
var moment_default = /*#__PURE__*/__webpack_require__.n(moment);

// EXTERNAL MODULE: ./connectedComponents/ConnectedHeader.js + 8 modules
var ConnectedHeader = __webpack_require__(1192);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react-i18next/dist/es/index.js + 9 modules
var dist_es = __webpack_require__(38);

// EXTERNAL MODULE: ./connectedComponents/ToolbarRow.css
var connectedComponents_ToolbarRow = __webpack_require__(1201);

// EXTERNAL MODULE: ./App.js + 33 modules
var App = __webpack_require__(301);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/cornerstone-tools/dist/cornerstoneTools.js
var cornerstoneTools = __webpack_require__(6);
var cornerstoneTools_default = /*#__PURE__*/__webpack_require__.n(cornerstoneTools);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/lodash.clonedeep/index.js
var lodash_clonedeep = __webpack_require__(43);
var lodash_clonedeep_default = /*#__PURE__*/__webpack_require__.n(lodash_clonedeep);

// CONCATENATED MODULE: ./connectedComponents/ConnectedCineDialog.js




 // Our target output kills the `as` and "import" throws a keyword error
// import { import as toolImport, getToolState } from 'cornerstone-tools';


var toolImport = cornerstoneTools_default.a.import;
var scrollToIndex = toolImport('util/scrollToIndex');
var setViewportSpecificData = core_src["a" /* default */].redux.actions.setViewportSpecificData; // Why do I need or care about any of this info?
// A dispatch action should be able to pull this at the time of an event?
// `isPlaying` and `cineFrameRate` might matter, but I think we can prop pass for those.

var ConnectedCineDialog_mapStateToProps = function mapStateToProps(state) {
  // Get activeViewport's `cine` and `stack`
  var _state$viewports = state.viewports,
      viewportSpecificData = _state$viewports.viewportSpecificData,
      activeViewportIndex = _state$viewports.activeViewportIndex;

  var _ref = viewportSpecificData[activeViewportIndex] || {},
      cine = _ref.cine;

  var dom = App["a" /* commandsManager */].runCommand('getActiveViewportEnabledElement');
  var cineData = cine || {
    isPlaying: false,
    cineFrameRate: 24
  }; // New props we're creating?

  return {
    activeEnabledElement: dom,
    activeViewportCineData: cineData,
    activeViewportIndex: state.viewports.activeViewportIndex
  };
};

var ConnectedCineDialog_mapDispatchToProps = function mapDispatchToProps(dispatch) {
  return {
    dispatchSetViewportSpecificData: function dispatchSetViewportSpecificData(viewportIndex, data) {
      dispatch(setViewportSpecificData(viewportIndex, data));
    }
  };
};

var ConnectedCineDialog_mergeProps = function mergeProps(propsFromState, propsFromDispatch, ownProps) {
  var activeEnabledElement = propsFromState.activeEnabledElement,
      activeViewportCineData = propsFromState.activeViewportCineData,
      activeViewportIndex = propsFromState.activeViewportIndex;
  return {
    cineFrameRate: activeViewportCineData.cineFrameRate,
    isPlaying: activeViewportCineData.isPlaying,
    onPlayPauseChanged: function onPlayPauseChanged(isPlaying) {
      var cine = lodash_clonedeep_default()(activeViewportCineData);
      cine.isPlaying = !cine.isPlaying;
      propsFromDispatch.dispatchSetViewportSpecificData(activeViewportIndex, {
        cine: cine
      });
    },
    onFrameRateChanged: function onFrameRateChanged(frameRate) {
      var cine = lodash_clonedeep_default()(activeViewportCineData);
      cine.cineFrameRate = frameRate;
      propsFromDispatch.dispatchSetViewportSpecificData(activeViewportIndex, {
        cine: cine
      });
    },
    onClickNextButton: function onClickNextButton() {
      var stackData = cornerstoneTools_default.a.getToolState(activeEnabledElement, 'stack');
      if (!stackData || !stackData.data || !stackData.data.length) return;
      var _stackData$data$ = stackData.data[0],
          currentImageIdIndex = _stackData$data$.currentImageIdIndex,
          imageIds = _stackData$data$.imageIds;
      if (currentImageIdIndex >= imageIds.length - 1) return;
      scrollToIndex(activeEnabledElement, currentImageIdIndex + 1);
    },
    onClickBackButton: function onClickBackButton() {
      var stackData = cornerstoneTools_default.a.getToolState(activeEnabledElement, 'stack');
      if (!stackData || !stackData.data || !stackData.data.length) return;
      var currentImageIdIndex = stackData.data[0].currentImageIdIndex;
      if (currentImageIdIndex === 0) return;
      scrollToIndex(activeEnabledElement, currentImageIdIndex - 1);
    },
    onClickSkipToStart: function onClickSkipToStart() {
      var stackData = cornerstoneTools_default.a.getToolState(activeEnabledElement, 'stack');
      if (!stackData || !stackData.data || !stackData.data.length) return;
      scrollToIndex(activeEnabledElement, 0);
    },
    onClickSkipToEnd: function onClickSkipToEnd() {
      var stackData = cornerstoneTools_default.a.getToolState(activeEnabledElement, 'stack');
      if (!stackData || !stackData.data || !stackData.data.length) return;
      var lastIndex = stackData.data[0].imageIds.length - 1;
      scrollToIndex(activeEnabledElement, lastIndex);
    }
  };
};

var ConnectedCineDialog = Object(es["b" /* connect */])(ConnectedCineDialog_mapStateToProps, ConnectedCineDialog_mapDispatchToProps, ConnectedCineDialog_mergeProps)(src["c" /* CineDialog */]);
/* harmony default export */ var connectedComponents_ConnectedCineDialog = (ConnectedCineDialog);
// CONCATENATED MODULE: ./connectedComponents/ConnectedLayoutButton.js



var _OHIF$redux$actions = core_src["a" /* default */].redux.actions,
    setLayout = _OHIF$redux$actions.setLayout,
    setViewportActive = _OHIF$redux$actions.setViewportActive;

var ConnectedLayoutButton_mapStateToProps = function mapStateToProps(state) {
  return {
    currentLayout: state.viewports.layout,
    activeViewportIndex: state.viewports.activeViewportIndex
  };
};

var ConnectedLayoutButton_mapDispatchToProps = function mapDispatchToProps(dispatch) {
  return {
    // TODO: Change if layout switched becomes more complex
    onChange: function onChange(selectedCell, currentLayout, activeViewportIndex) {
      var viewports = [];
      var numRows = selectedCell.row + 1;
      var numColumns = selectedCell.col + 1;
      var numViewports = numRows * numColumns;

      for (var i = 0; i < numViewports; i++) {
        // Hacky way to allow users to exit MPR "mode"
        var viewport = currentLayout.viewports[i];
        var plugin = viewport && viewport.plugin;

        if (viewport && viewport.vtk) {
          plugin = 'cornerstone';
        }

        viewports.push({
          plugin: plugin
        });
      }

      var layout = {
        numRows: numRows,
        numColumns: numColumns,
        viewports: viewports
      };
      var maxActiveIndex = numViewports - 1;

      if (activeViewportIndex > maxActiveIndex) {
        dispatch(setViewportActive(0));
      }

      dispatch(setLayout(layout));
    }
  };
};

var ConnectedLayoutButton_mergeProps = function mergeProps(propsFromState, propsFromDispatch) {
  var onChangeFromDispatch = propsFromDispatch.onChange;
  var currentLayout = propsFromState.currentLayout,
      activeViewportIndex = propsFromState.activeViewportIndex;
  return {
    onChange: function onChange(selectedCell) {
      return onChangeFromDispatch(selectedCell, currentLayout, activeViewportIndex);
    }
  };
};

var ConnectedLayoutButton = Object(es["b" /* connect */])(ConnectedLayoutButton_mapStateToProps, ConnectedLayoutButton_mapDispatchToProps, ConnectedLayoutButton_mergeProps)(src["m" /* LayoutButton */]);
/* harmony default export */ var connectedComponents_ConnectedLayoutButton = (ConnectedLayoutButton);
// EXTERNAL MODULE: ./context/AppContext.js
var AppContext = __webpack_require__(89);

// CONCATENATED MODULE: ./connectedComponents/ToolbarRow.js
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance"); }

function _iterableToArray(iter) { if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }












var ToolbarRow_ToolbarRow =
/*#__PURE__*/
function (_Component) {
  _inherits(ToolbarRow, _Component);

  // TODO: Simplify these? isOpen can be computed if we say "any" value for selected,
  // closed if selected is null/undefined
  function ToolbarRow(props) {
    var _this2;

    _classCallCheck(this, ToolbarRow);

    _this2 = _possibleConstructorReturn(this, _getPrototypeOf(ToolbarRow).call(this, props));

    _defineProperty(_assertThisInitialized(_this2), "closeCineDialogIfNotApplicable", function () {
      var dialog = _this2.props.dialog;
      var _this2$state = _this2.state,
          dialogId = _this2$state.dialogId,
          activeButtons = _this2$state.activeButtons,
          toolbarButtons = _this2$state.toolbarButtons;

      if (dialogId) {
        var cineButtonPresent = toolbarButtons.find(function (button) {
          return button.options && button.options.behavior === 'CINE';
        });

        if (!cineButtonPresent) {
          dialog.dismiss({
            id: dialogId
          });
          activeButtons = activeButtons.filter(function (button) {
            return button.options && button.options.behavior !== 'CINE';
          });

          _this2.setState({
            dialogId: null,
            activeButtons: activeButtons
          });
        }
      }
    });

    var toolbarButtonDefinitions = _getVisibleToolbarButtons.call(_assertThisInitialized(_this2)); // TODO:
    // If it's a tool that can be active... Mark it as active?
    // - Tools that are on/off?
    // - Tools that can be bound to multiple buttons?
    // Normal ToolbarButtons...
    // Just how high do we need to hoist this state?
    // Why ToolbarRow instead of just Toolbar? Do we have any others?


    _this2.state = {
      toolbarButtons: toolbarButtonDefinitions,
      activeButtons: []
    };
    _this2.seriesPerStudyCount = [];
    _this2._handleBuiltIn = _handleBuiltIn.bind(_assertThisInitialized(_this2));
    _this2._onDerivedDisplaySetsLoadedAndCached = _this2._onDerivedDisplaySetsLoadedAndCached.bind(_assertThisInitialized(_this2));

    _this2.updateButtonGroups();

    return _this2;
  }

  _createClass(ToolbarRow, [{
    key: "updateButtonGroups",
    value: function updateButtonGroups() {
      var _this3 = this;

      var panelModules = App["c" /* extensionManager */].modules[MODULE_TYPES["a" /* default */].PANEL];
      this.buttonGroups = {
        left: [],
        right: []
      }; // ~ FIND MENU OPTIONS

      panelModules.forEach(function (panelExtension) {
        var panelModule = panelExtension.module;
        var defaultContexts = Array.from(panelModule.defaultContext);
        panelModule.menuOptions.forEach(function (menuOption) {
          var contexts = Array.from(menuOption.context || defaultContexts);

          var hasActiveContext = _this3.props.activeContexts.some(function (actx) {
            return contexts.includes(actx);
          }); // It's a bit beefy to pass studies; probably only need to be reactive on `studyInstanceUIDs` and activeViewport?
          // Note: This does not cleanly handle `studies` prop updating with panel open


          var isDisabled = typeof menuOption.isDisabled === 'function' && menuOption.isDisabled(_this3.props.studies, _this3.props.activeViewport);

          if (hasActiveContext && !isDisabled) {
            var menuOptionEntry = {
              value: menuOption.target,
              icon: menuOption.icon,
              bottomLabel: menuOption.label
            };
            var from = menuOption.from || 'right';

            _this3.buttonGroups[from].push(menuOptionEntry);
          }
        });
      }); // TODO: This should come from extensions, instead of being baked in

      this.buttonGroups.left.unshift({
        value: 'studies',
        icon: 'th-large',
        bottomLabel: this.props.t('Series')
      });
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      /*
       * TODO: Improve the way we notify parts of the app
       * that depends on derived display sets to be loaded.
       * (Implement pubsub for better tracking of derived display sets)
       */
      document.addEventListener('deriveddisplaysetsloadedandcached', this._onDerivedDisplaySetsLoadedAndCached);
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      document.removeEventListener('deriveddisplaysetsloadedandcached', this._onDerivedDisplaySetsLoadedAndCached);
    }
  }, {
    key: "_onDerivedDisplaySetsLoadedAndCached",
    value: function _onDerivedDisplaySetsLoadedAndCached() {
      this.updateButtonGroups();
      this.setState({
        toolbarButtons: _getVisibleToolbarButtons.call(this)
      });
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate(prevProps) {
      var activeContextsChanged = prevProps.activeContexts !== this.props.activeContexts;
      var prevStudies = prevProps.studies;
      var prevActiveViewport = prevProps.activeViewport;
      var activeViewport = this.props.activeViewport;
      var studies = this.props.studies;
      var seriesPerStudyCount = this.seriesPerStudyCount;
      var shouldUpdate = false;

      if (prevStudies.length !== studies.length || prevActiveViewport !== activeViewport) {
        shouldUpdate = true;
      } else {
        for (var i = 0; i < studies.length; i++) {
          if (studies[i].series.length !== seriesPerStudyCount[i]) {
            seriesPerStudyCount[i] = studies[i].series.length;
            shouldUpdate = true;
            break;
          }
        }
      }

      if (shouldUpdate) {
        this.updateButtonGroups();
      }

      if (activeContextsChanged) {
        this.setState({
          toolbarButtons: _getVisibleToolbarButtons.call(this)
        }, this.closeCineDialogIfNotApplicable);
      }
    }
  }, {
    key: "render",
    value: function render() {
      var _this4 = this;

      var buttonComponents = _getButtonComponents.call(this, this.state.toolbarButtons, this.state.activeButtons);

      var onPress = function onPress(side, value) {
        _this4.props.handleSidePanelChange(side, value);
      };

      var onPressLeft = onPress.bind(this, 'left');
      var onPressRight = onPress.bind(this, 'right');
      return react_default.a.createElement(react_default.a.Fragment, null, react_default.a.createElement("div", {
        className: "ToolbarRow"
      }, react_default.a.createElement("div", {
        className: "pull-left m-t-1 p-y-1",
        style: {
          padding: '10px'
        }
      }, react_default.a.createElement(src["v" /* RoundedButtonGroup */], {
        options: this.buttonGroups.left,
        value: this.props.selectedLeftSidePanel || '',
        onValueChanged: onPressLeft
      })), buttonComponents, react_default.a.createElement(connectedComponents_ConnectedLayoutButton, null), react_default.a.createElement("div", {
        className: "pull-right m-t-1 rm-x-1",
        style: {
          marginLeft: 'auto'
        }
      }, this.buttonGroups.right.length && react_default.a.createElement(src["v" /* RoundedButtonGroup */], {
        options: this.buttonGroups.right,
        value: this.props.selectedRightSidePanel || '',
        onValueChanged: onPressRight
      }))));
    }
  }]);

  return ToolbarRow;
}(react["Component"]);

_defineProperty(ToolbarRow_ToolbarRow, "propTypes", {
  isLeftSidePanelOpen: prop_types_default.a.bool.isRequired,
  isRightSidePanelOpen: prop_types_default.a.bool.isRequired,
  selectedLeftSidePanel: prop_types_default.a.string.isRequired,
  selectedRightSidePanel: prop_types_default.a.string.isRequired,
  handleSidePanelChange: prop_types_default.a.func.isRequired,
  activeContexts: prop_types_default.a.arrayOf(prop_types_default.a.string).isRequired,
  studies: prop_types_default.a.array,
  t: prop_types_default.a.func.isRequired,
  // NOTE: withDialog, withModal HOCs
  dialog: prop_types_default.a.any,
  modal: prop_types_default.a.any
});

_defineProperty(ToolbarRow_ToolbarRow, "defaultProps", {
  studies: []
});

function _getCustomButtonComponent(button, activeButtons) {
  var CustomComponent = button.CustomComponent;
  var isValidComponent = typeof CustomComponent === 'function'; // Check if its a valid customComponent. Later on an CustomToolbarComponent interface could be implemented.

  if (isValidComponent) {
    var parentContext = this;
    var activeButtonsIds = activeButtons.map(function (button) {
      return button.id;
    });
    var isActive = activeButtonsIds.includes(button.id);
    return react_default.a.createElement(CustomComponent, {
      parentContext: parentContext,
      toolbarClickCallback: _handleToolbarButtonClick.bind(this),
      button: button,
      key: button.id,
      activeButtons: activeButtonsIds,
      isActive: isActive
    });
  }
}

function _getExpandableButtonComponent(button, activeButtons) {
  var _this5 = this;

  // Iterate over button definitions and update `onClick` behavior
  var activeCommand;
  var childButtons = button.buttons.map(function (childButton) {
    childButton.onClick = _handleToolbarButtonClick.bind(_this5, childButton);

    if (activeButtons.map(function (button) {
      return button.id;
    }).indexOf(childButton.id) > -1) {
      activeCommand = childButton.id;
    }

    return childButton;
  });
  return react_default.a.createElement(src["i" /* ExpandableToolMenu */], {
    key: button.id,
    label: button.label,
    icon: button.icon,
    buttons: childButtons,
    activeCommand: activeCommand
  });
}

function _getDefaultButtonComponent(button, activeButtons) {
  return react_default.a.createElement(src["J" /* ToolbarButton */], {
    key: button.id,
    label: button.label,
    icon: button.icon,
    onClick: _handleToolbarButtonClick.bind(this, button),
    isActive: activeButtons.map(function (button) {
      return button.id;
    }).includes(button.id)
  });
}
/**
 * Determine which extension buttons should be showing, if they're
 * active, and what their onClick behavior should be.
 */


function _getButtonComponents(toolbarButtons, activeButtons) {
  var _this = this;

  return toolbarButtons.map(function (button) {
    var hasCustomComponent = button.CustomComponent;
    var hasNestedButtonDefinitions = button.buttons && button.buttons.length;

    if (hasCustomComponent) {
      return _getCustomButtonComponent.call(_this, button, activeButtons);
    }

    if (hasNestedButtonDefinitions) {
      return _getExpandableButtonComponent.call(_this, button, activeButtons);
    }

    return _getDefaultButtonComponent.call(_this, button, activeButtons);
  });
}
/**
 * TODO: DEPRECATE
 * This is used exclusively in `extensions/cornerstone/src`
 * We have better ways with new UI Services to trigger "builtin" behaviors
 *
 * A handy way for us to handle different button types. IE. firing commands for
 * buttons, or initiation built in behavior.
 *
 * @param {*} button
 * @param {*} evt
 * @param {*} props
 */


function _handleToolbarButtonClick(button, evt, props) {
  var activeButtons = this.state.activeButtons;

  if (button.commandName) {
    var options = Object.assign({
      evt: evt
    }, button.commandOptions);
    App["a" /* commandsManager */].runCommand(button.commandName, options);
  } // TODO: Use Types ENUM
  // TODO: We can update this to be a `getter` on the extension to query
  //       For the active tools after we apply our updates?


  if (button.type === 'setToolActive') {
    var toggables = activeButtons.filter(function (_ref) {
      var options = _ref.options;
      return options && !options.togglable;
    });
    this.setState({
      activeButtons: [].concat(_toConsumableArray(toggables), [button])
    });
  } else if (button.type === 'builtIn') {
    this._handleBuiltIn(button);
  }
}
/**
 *
 */


function _getVisibleToolbarButtons() {
  var _this6 = this;

  var toolbarModules = App["c" /* extensionManager */].modules[MODULE_TYPES["a" /* default */].TOOLBAR];
  var toolbarButtonDefinitions = [];
  toolbarModules.forEach(function (extension) {
    var _extension$module = extension.module,
        definitions = _extension$module.definitions,
        defaultContext = _extension$module.defaultContext;
    definitions.forEach(function (definition) {
      var context = definition.context || defaultContext;

      if (_this6.props.activeContexts.includes(context)) {
        toolbarButtonDefinitions.push(definition);
      }
    });
  });
  return toolbarButtonDefinitions;
}

function _handleBuiltIn(button) {
  /* TODO: Keep cine button active until its unselected. */
  var _this$props = this.props,
      dialog = _this$props.dialog,
      t = _this$props.t;
  var dialogId = this.state.dialogId;
  var id = button.id,
      options = button.options;

  if (options.behavior === 'CINE') {
    if (dialogId) {
      dialog.dismiss({
        id: dialogId
      });
      this.setState(function (state) {
        return {
          dialogId: null,
          activeButtons: _toConsumableArray(state.activeButtons.filter(function (button) {
            return button.id !== id;
          }))
        };
      });
    } else {
      var spacing = 20;

      var _document$querySelect = document.querySelector(".ViewerMain").getBoundingClientRect(),
          x = _document$querySelect.x,
          y = _document$querySelect.y;

      var newDialogId = dialog.create({
        content: connectedComponents_ConnectedCineDialog,
        defaultPosition: {
          x: x + spacing || 0,
          y: y + spacing || 0
        }
      });
      this.setState(function (state) {
        return {
          dialogId: newDialogId,
          activeButtons: [].concat(_toConsumableArray(state.activeButtons), [button])
        };
      });
    }
  }

  if (options.behavior === 'DOWNLOAD_SCREEN_SHOT') {
    App["a" /* commandsManager */].runCommand('showDownloadViewportModal', {
      title: t('Download High Quality Image')
    });
  }
}

/* harmony default export */ var connectedComponents_ToolbarRow_0 = (Object(dist_es["d" /* withTranslation */])(['Common', 'ViewportDownloadForm'])(Object(src["U" /* withModal */])(Object(src["T" /* withDialog */])(Object(AppContext["e" /* withAppContext */])(ToolbarRow_ToolbarRow)))));
// CONCATENATED MODULE: ./connectedComponents/findDisplaySetByUID.js
/**
 * Finds displaySet by UID across all displaySets inside studyMetadata
 * @param {Array} studyMetadata
 * @param {string} displaySetInstanceUID
 */
function findDisplaySetByUID(studyMetadata, displaySetInstanceUID) {
  if (!Array.isArray(studyMetadata)) return null;
  var allDisplaySets = studyMetadata.reduce(function (all, current) {
    var currentDisplaySet = [];

    if (current && Array.isArray(current.displaySets)) {
      currentDisplaySet = current.displaySets;
    }

    return all.concat(currentDisplaySet);
  }, []);

  var bySetInstanceUID = function bySetInstanceUID(ds) {
    return ds.displaySetInstanceUID === displaySetInstanceUID;
  };

  var displaySet = allDisplaySets.find(bySetInstanceUID);
  return displaySet || null;
}
// CONCATENATED MODULE: ./connectedComponents/ConnectedStudyBrowser.js






var studyMetadataManager = core_src["a" /* default */].utils.studyMetadataManager;
var setActiveViewportSpecificData = core_src["a" /* default */].redux.actions.setActiveViewportSpecificData; // TODO
// - Determine in which display set is active from Redux (activeViewportIndex and layout viewportData)
// - Pass in errors and stack loading progress from Redux

var ConnectedStudyBrowser_mapStateToProps = function mapStateToProps(state, ownProps) {
  // If we know that the stack loading progress details have changed,
  // we can try to update the component state so that the thumbnail
  // progress bar is updated
  var stackLoadingProgressMap = state.loading.progress;
  var studiesWithLoadingData = lodash_clonedeep_default()(ownProps.studies);
  studiesWithLoadingData.forEach(function (study) {
    study.thumbnails.forEach(function (data) {
      var displaySetInstanceUID = data.displaySetInstanceUID;
      var stackId = "StackProgress:".concat(displaySetInstanceUID);
      var stackProgressData = stackLoadingProgressMap[stackId];
      var stackPercentComplete = 0;

      if (stackProgressData) {
        stackPercentComplete = stackProgressData.percentComplete;
      }

      data.stackPercentComplete = stackPercentComplete;
    });
  });
  return {
    studies: studiesWithLoadingData
  };
};

var ConnectedStudyBrowser_mapDispatchToProps = function mapDispatchToProps(dispatch, ownProps) {
  return {
    onThumbnailClick: function onThumbnailClick(displaySetInstanceUID) {
      var displaySet = findDisplaySetByUID(ownProps.studyMetadata, displaySetInstanceUID);

      if (displaySet.isDerived) {
        var _displaySet = displaySet,
            Modality = _displaySet.Modality;

        if (Modality === 'SEG' && App["e" /* servicesManager */]) {
          var _servicesManager$serv = App["e" /* servicesManager */].services,
              LoggerService = _servicesManager$serv.LoggerService,
              UINotificationService = _servicesManager$serv.UINotificationService;

          var onDisplaySetLoadFailureHandler = function onDisplaySetLoadFailureHandler(error) {
            LoggerService.error({
              error: error,
              message: error.message
            });
            UINotificationService.show({
              title: 'DICOM Segmentation Loader',
              message: error.message,
              type: 'error',
              autoClose: true
            });
          };

          var _displaySet$getSource = displaySet.getSourceDisplaySet(ownProps.studyMetadata, true, onDisplaySetLoadFailureHandler),
              referencedDisplaySet = _displaySet$getSource.referencedDisplaySet,
              activatedLabelmapPromise = _displaySet$getSource.activatedLabelmapPromise;

          displaySet = referencedDisplaySet;
          activatedLabelmapPromise.then(function (activatedLabelmapIndex) {
            var selectionFired = new CustomEvent("extensiondicomsegmentationsegselected", {
              "detail": {
                "activatedLabelmapIndex": activatedLabelmapIndex
              }
            });
            document.dispatchEvent(selectionFired);
          });
        } else {
          displaySet = displaySet.getSourceDisplaySet(ownProps.studyMetadata);
        }

        if (!displaySet) {
          throw new Error("Referenced series for ".concat(Modality, " dataset not present."));
        }

        if (!displaySet) {
          throw new Error('Source data not present');
        }
      }

      dispatch(setActiveViewportSpecificData(displaySet));
    }
  };
};

var ConnectedStudyBrowser = Object(es["b" /* connect */])(ConnectedStudyBrowser_mapStateToProps, ConnectedStudyBrowser_mapDispatchToProps)(src["B" /* StudyBrowser */]);
/* harmony default export */ var connectedComponents_ConnectedStudyBrowser = (ConnectedStudyBrowser);
// EXTERNAL MODULE: ./connectedComponents/ViewerMain.css
var connectedComponents_ViewerMain = __webpack_require__(1202);

// EXTERNAL MODULE: ./components/ViewportGrid/ViewportGrid.css
var ViewportGrid_ViewportGrid = __webpack_require__(1203);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/core/src/utils/index.js + 15 modules
var utils = __webpack_require__(156);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react-dnd/dist/esm/index.js + 31 modules
var esm = __webpack_require__(224);

// EXTERNAL MODULE: ./components/ViewportGrid/ViewportPane.css
var ViewportGrid_ViewportPane = __webpack_require__(1204);

// CONCATENATED MODULE: ./components/ViewportGrid/ViewportPane.js
function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { if (!(Symbol.iterator in Object(arr) || Object.prototype.toString.call(arr) === "[object Arguments]")) { return; } var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }







var ViewportPane_ViewportPane = function ViewportPane(props) {
  var children = props.children,
      onDrop = props.onDrop,
      viewportIndex = props.viewportIndex,
      propClassName = props.className;

  var _useDrop = Object(esm["d" /* useDrop */])({
    accept: 'thumbnail',
    drop: function drop(droppedItem, monitor) {
      var canDrop = monitor.canDrop();
      var isOver = monitor.isOver();

      if (canDrop && isOver && onDrop) {
        var StudyInstanceUID = droppedItem.StudyInstanceUID,
            displaySetInstanceUID = droppedItem.displaySetInstanceUID;
        onDrop({
          viewportIndex: viewportIndex,
          StudyInstanceUID: StudyInstanceUID,
          displaySetInstanceUID: displaySetInstanceUID
        });
      }
    },
    // Monitor, and collect props.
    // Returned as values by `useDrop`
    collect: function collect(monitor) {
      return {
        highlighted: monitor.canDrop(),
        hovered: monitor.isOver()
      };
    }
  }),
      _useDrop2 = _slicedToArray(_useDrop, 2),
      _useDrop2$ = _useDrop2[0],
      hovered = _useDrop2$.hovered,
      highlighted = _useDrop2$.highlighted,
      drop = _useDrop2[1];

  return react_default.a.createElement("div", {
    className: classnames_default()('viewport-drop-target', {
      hovered: hovered
    }, {
      highlighted: highlighted
    }, propClassName),
    ref: drop,
    "data-cy": "viewport-container-".concat(viewportIndex)
  }, children);
};

ViewportPane_ViewportPane.propTypes = {
  children: prop_types_default.a.node.isRequired,
  viewportIndex: prop_types_default.a.number.isRequired,
  onDrop: prop_types_default.a.func.isRequired,
  className: prop_types_default.a.string
};
/* harmony default export */ var components_ViewportGrid_ViewportPane = (ViewportPane_ViewportPane);
// CONCATENATED MODULE: ./components/ViewportGrid/DefaultViewport.js
/**
 *
 *
 * @export
 * @param {*} props
 * @returns
 */
function DefaultViewport(props) {
  return React.createElement("div", null, JSON.stringify(props));
}
// EXTERNAL MODULE: ./components/ViewportGrid/EmptyViewport.js
var EmptyViewport = __webpack_require__(1205);
var EmptyViewport_default = /*#__PURE__*/__webpack_require__.n(EmptyViewport);

// CONCATENATED MODULE: ./components/ViewportGrid/ViewportGrid.js





 //




var loadAndCacheDerivedDisplaySets = utils["a" /* default */].loadAndCacheDerivedDisplaySets;

var ViewportGrid_ViewportGrid_ViewportGrid = function ViewportGrid(props) {
  var activeViewportIndex = props.activeViewportIndex,
      availablePlugins = props.availablePlugins,
      defaultPluginName = props.defaultPlugin,
      layout = props.layout,
      numRows = props.numRows,
      numColumns = props.numColumns,
      setViewportData = props.setViewportData,
      studies = props.studies,
      viewportData = props.viewportData,
      children = props.children,
      isStudyLoaded = props.isStudyLoaded;
  var rowSize = 100 / numRows;
  var colSize = 100 / numColumns; // http://grid.malven.co/

  if (!viewportData || !viewportData.length) {
    return null;
  }

  var snackbar = Object(src["S" /* useSnackbarContext */])();
  var logger = Object(src["Q" /* useLogger */])();
  Object(react["useEffect"])(function () {
    if (isStudyLoaded) {
      viewportData.forEach(function (displaySet) {
        loadAndCacheDerivedDisplaySets(displaySet, studies, logger, snackbar);
      });
    }
  }, [studies, viewportData, isStudyLoaded, snackbar]);

  var getViewportPanes = function getViewportPanes() {
    return layout.viewports.map(function (layout, viewportIndex) {
      var displaySet = viewportData[viewportIndex];

      if (!displaySet) {
        return null;
      }

      var data = {
        displaySet: displaySet,
        studies: studies
      }; // JAMES TODO:
      // Use whichever plugin is currently in use in the panel
      // unless nothing is specified. If nothing is specified
      // and the display set has a plugin specified, use that.
      //
      // TODO: Change this logic to:
      // - Plugins define how capable they are of displaying a SopClass
      // - When updating a panel, ensure that the currently enabled plugin
      // in the viewport is capable of rendering this display set. If not
      // then use the most capable available plugin

      var pluginName = !layout.plugin && displaySet && displaySet.plugin ? displaySet.plugin : layout.plugin;

      var ViewportComponent = _getViewportComponent(data, // Why do we pass this as `ViewportData`, when that's not really what it is?
      viewportIndex, children, availablePlugins, pluginName, defaultPluginName);

      return react_default.a.createElement(components_ViewportGrid_ViewportPane, {
        onDrop: setViewportData,
        viewportIndex: viewportIndex // Needed by `setViewportData`
        ,
        className: classnames_default()('viewport-container', {
          active: activeViewportIndex === viewportIndex
        }),
        key: viewportIndex
      }, ViewportComponent);
    });
  };

  var ViewportPanes = react_default.a.useMemo(getViewportPanes, [layout, viewportData, studies, children, availablePlugins, defaultPluginName, setViewportData, activeViewportIndex]);
  return react_default.a.createElement("div", {
    "data-cy": "viewprt-grid",
    style: {
      display: 'grid',
      gridTemplateRows: "repeat(".concat(numRows, ", ").concat(rowSize, "%)"),
      gridTemplateColumns: "repeat(".concat(numColumns, ", ").concat(colSize, "%)"),
      height: '100%',
      width: '100%'
    }
  }, ViewportPanes);
};

ViewportGrid_ViewportGrid_ViewportGrid.propTypes = {
  viewportData: prop_types_default.a.array.isRequired,
  supportsDrop: prop_types_default.a.bool.isRequired,
  activeViewportIndex: prop_types_default.a.number.isRequired,
  layout: prop_types_default.a.object.isRequired,
  availablePlugins: prop_types_default.a.object.isRequired,
  setViewportData: prop_types_default.a.func.isRequired,
  studies: prop_types_default.a.array,
  children: prop_types_default.a.node,
  defaultPlugin: prop_types_default.a.string,
  numRows: prop_types_default.a.number.isRequired,
  numColumns: prop_types_default.a.number.isRequired
};
ViewportGrid_ViewportGrid_ViewportGrid.defaultProps = {
  viewportData: [],
  numRows: 1,
  numColumns: 1,
  layout: {
    viewports: [{}]
  },
  activeViewportIndex: 0,
  supportsDrop: true,
  availablePlugins: {
    DefaultViewport: DefaultViewport
  },
  defaultPlugin: 'defaultViewportPlugin'
};
/**
 *
 *
 * @param {*} plugin
 * @param {*} viewportData
 * @param {*} viewportIndex
 * @param {*} children
 * @returns
 */

function _getViewportComponent(viewportData, viewportIndex, children, availablePlugins, pluginName, defaultPluginName) {
  if (viewportData.displaySet) {
    pluginName = pluginName || defaultPluginName;
    var ViewportComponent = availablePlugins[pluginName];

    if (!ViewportComponent) {
      throw new Error("No Viewport Component available for name ".concat(pluginName, ".\n         Available plugins: ").concat(JSON.stringify(availablePlugins)));
    }

    return react_default.a.createElement(ViewportComponent, {
      viewportData: viewportData,
      viewportIndex: viewportIndex,
      children: [children]
    });
  }

  return react_default.a.createElement(EmptyViewport_default.a, null);
}

/* harmony default export */ var components_ViewportGrid_ViewportGrid = (ViewportGrid_ViewportGrid_ViewportGrid);
// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/lodash/memoize.js
var memoize = __webpack_require__(722);
var memoize_default = /*#__PURE__*/__webpack_require__.n(memoize);

// CONCATENATED MODULE: ./components/ViewportGrid/ConnectedViewportGrid.js





var getAvailableViewportModules = memoize_default()(function (viewportModules) {
  var availableViewportModules = {};
  viewportModules.forEach(function (moduleDefinition) {
    availableViewportModules[moduleDefinition.extensionId] = moduleDefinition.module;
  });
  return availableViewportModules;
});

var ConnectedViewportGrid_mapStateToProps = function mapStateToProps(state) {
  var viewportModules = App["c" /* extensionManager */].modules[MODULE_TYPES["a" /* default */].VIEWPORT];
  var availableViewportModules = getAvailableViewportModules(viewportModules); // TODO: Use something like state.plugins.defaultPlugin[MODULE_TYPES.VIEWPORT]

  var defaultPlugin;

  if (viewportModules.length) {
    defaultPlugin = viewportModules[0].extensionId;
  }

  var _state$viewports = state.viewports,
      numRows = _state$viewports.numRows,
      numColumns = _state$viewports.numColumns,
      layout = _state$viewports.layout,
      activeViewportIndex = _state$viewports.activeViewportIndex;
  return {
    numRows: numRows,
    numColumns: numColumns,
    layout: layout,
    activeViewportIndex: activeViewportIndex,
    // TODO: rename `availableViewportModules`
    availablePlugins: availableViewportModules,
    // TODO: rename `defaultViewportModule`
    defaultPlugin: defaultPlugin
  };
};

var ConnectedViewportGrid = Object(es["b" /* connect */])(ConnectedViewportGrid_mapStateToProps, null)(components_ViewportGrid_ViewportGrid);
/* harmony default export */ var ViewportGrid_ConnectedViewportGrid = (ConnectedViewportGrid);
// CONCATENATED MODULE: ./components/ViewportGrid/index.js


/* harmony default export */ var components_ViewportGrid = (components_ViewportGrid_ViewportGrid);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/lodash/values.js
var values = __webpack_require__(1183);
var values_default = /*#__PURE__*/__webpack_require__.n(values);

// CONCATENATED MODULE: ./connectedComponents/ViewerMain.js
function ViewerMain_typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { ViewerMain_typeof = function _typeof(obj) { return typeof obj; }; } else { ViewerMain_typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return ViewerMain_typeof(obj); }

function ViewerMain_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function ViewerMain_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function ViewerMain_createClass(Constructor, protoProps, staticProps) { if (protoProps) ViewerMain_defineProperties(Constructor.prototype, protoProps); if (staticProps) ViewerMain_defineProperties(Constructor, staticProps); return Constructor; }

function ViewerMain_possibleConstructorReturn(self, call) { if (call && (ViewerMain_typeof(call) === "object" || typeof call === "function")) { return call; } return ViewerMain_assertThisInitialized(self); }

function ViewerMain_getPrototypeOf(o) { ViewerMain_getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return ViewerMain_getPrototypeOf(o); }

function ViewerMain_assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function ViewerMain_inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) ViewerMain_setPrototypeOf(subClass, superClass); }

function ViewerMain_setPrototypeOf(o, p) { ViewerMain_setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return ViewerMain_setPrototypeOf(o, p); }

function ViewerMain_defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }









var ViewerMain_values = memoize_default()(values_default.a);

var ViewerMain_ViewerMain =
/*#__PURE__*/
function (_Component) {
  ViewerMain_inherits(ViewerMain, _Component);

  function ViewerMain(props) {
    var _this;

    ViewerMain_classCallCheck(this, ViewerMain);

    _this = ViewerMain_possibleConstructorReturn(this, ViewerMain_getPrototypeOf(ViewerMain).call(this, props));

    ViewerMain_defineProperty(ViewerMain_assertThisInitialized(_this), "fillEmptyViewportPanes", function () {
      // TODO: Here is the entry point for filling viewports on load.
      var dirtyViewportPanes = [];
      var _this$props = _this.props,
          layout = _this$props.layout,
          viewportSpecificData = _this$props.viewportSpecificData;
      var displaySets = _this.state.displaySets;

      if (!displaySets || !displaySets.length) {
        return;
      }

      for (var i = 0; i < layout.viewports.length; i++) {
        var viewportPane = viewportSpecificData[i];
        var isNonEmptyViewport = viewportPane && viewportPane.StudyInstanceUID && viewportPane.displaySetInstanceUID;

        if (isNonEmptyViewport) {
          dirtyViewportPanes.push({
            StudyInstanceUID: viewportPane.StudyInstanceUID,
            displaySetInstanceUID: viewportPane.displaySetInstanceUID
          });
          continue;
        }

        var foundDisplaySet = displaySets.find(function (ds) {
          return !dirtyViewportPanes.some(function (v) {
            return v.displaySetInstanceUID === ds.displaySetInstanceUID;
          });
        }) || displaySets[displaySets.length - 1];
        dirtyViewportPanes.push(foundDisplaySet);
      }

      dirtyViewportPanes.forEach(function (vp, i) {
        if (vp && vp.StudyInstanceUID) {
          _this.setViewportData({
            viewportIndex: i,
            StudyInstanceUID: vp.StudyInstanceUID,
            displaySetInstanceUID: vp.displaySetInstanceUID
          });
        }
      });
    });

    ViewerMain_defineProperty(ViewerMain_assertThisInitialized(_this), "setViewportData", function (_ref) {
      var viewportIndex = _ref.viewportIndex,
          StudyInstanceUID = _ref.StudyInstanceUID,
          displaySetInstanceUID = _ref.displaySetInstanceUID;

      var displaySet = _this.findDisplaySet(_this.props.studies, StudyInstanceUID, displaySetInstanceUID);

      if (displaySet.isDerived) {
        var _displaySet = displaySet,
            Modality = _displaySet.Modality;

        if (Modality === 'SEG' && App["e" /* servicesManager */]) {
          var _servicesManager$serv = App["e" /* servicesManager */].services,
              LoggerService = _servicesManager$serv.LoggerService,
              UINotificationService = _servicesManager$serv.UINotificationService;

          var onDisplaySetLoadFailureHandler = function onDisplaySetLoadFailureHandler(error) {
            LoggerService.error({
              error: error,
              message: error.message
            });
            UINotificationService.show({
              title: 'DICOM Segmentation Loader',
              message: error.message,
              type: 'error',
              autoClose: true
            });
          };

          var _displaySet$getSource = displaySet.getSourceDisplaySet(_this.props.studies, true, onDisplaySetLoadFailureHandler),
              referencedDisplaySet = _displaySet$getSource.referencedDisplaySet;

          displaySet = referencedDisplaySet;
        } else {
          displaySet = displaySet.getSourceDisplaySet(_this.props.studies);
        }

        if (!displaySet) {
          throw new Error("Referenced series for ".concat(Modality, " dataset not present."));
        }
      }

      _this.props.setViewportSpecificData(viewportIndex, displaySet);
    });

    _this.state = {
      displaySets: []
    };
    return _this;
  }

  ViewerMain_createClass(ViewerMain, [{
    key: "getDisplaySets",
    value: function getDisplaySets(studies) {
      var displaySets = [];
      studies.forEach(function (study) {
        study.displaySets.forEach(function (dSet) {
          if (!dSet.plugin) {
            dSet.plugin = 'cornerstone';
          }

          displaySets.push(dSet);
        });
      });
      return displaySets;
    }
  }, {
    key: "findDisplaySet",
    value: function findDisplaySet(studies, StudyInstanceUID, displaySetInstanceUID) {
      var study = studies.find(function (study) {
        return study.StudyInstanceUID === StudyInstanceUID;
      });

      if (!study) {
        return;
      }

      return study.displaySets.find(function (displaySet) {
        return displaySet.displaySetInstanceUID === displaySetInstanceUID;
      });
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      // Add beforeUnload event handler to check for unsaved changes
      //window.addEventListener('beforeunload', unloadHandlers.beforeUnload);
      // Get all the display sets for the viewer studies
      if (this.props.studies) {
        var displaySets = this.getDisplaySets(this.props.studies);
        this.setState({
          displaySets: displaySets
        }, this.fillEmptyViewportPanes);
      }
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate(prevProps) {
      var prevViewportAmount = prevProps.layout.viewports.length;
      var viewportAmount = this.props.layout.viewports.length;
      var isVtk = this.props.layout.viewports.some(function (vp) {
        return !!vp.vtk;
      });

      if (this.props.studies !== prevProps.studies || viewportAmount !== prevViewportAmount && !isVtk) {
        var displaySets = this.getDisplaySets(this.props.studies);
        this.setState({
          displaySets: displaySets
        }, this.fillEmptyViewportPanes);
      }
    }
  }, {
    key: "render",
    value: function render() {
      var viewportSpecificData = this.props.viewportSpecificData;
      var viewportData = ViewerMain_values(viewportSpecificData);
      return react_default.a.createElement("div", {
        className: "ViewerMain"
      }, this.state.displaySets.length && react_default.a.createElement(ViewportGrid_ConnectedViewportGrid, {
        isStudyLoaded: this.props.isStudyLoaded,
        studies: this.props.studies,
        viewportData: viewportData,
        setViewportData: this.setViewportData
      }));
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      var _this2 = this;

      // Clear the entire viewport specific data
      var viewportSpecificData = this.props.viewportSpecificData;
      Object.keys(viewportSpecificData).forEach(function (viewportIndex) {
        _this2.props.clearViewportSpecificData(viewportIndex);
      }); // TODO: These don't have to be viewer specific?
      // Could qualify for other routes?
      // hotkeys.destroy();
      // Remove beforeUnload event handler...
      //window.removeEventListener('beforeunload', unloadHandlers.beforeUnload);
      // Destroy the synchronizer used to update reference lines
      //OHIF.viewer.updateImageSynchronizer.destroy();
      // TODO: Instruct all plugins to clean up themselves
      //
      // Clear references to all stacks in the StackManager
      //StackManager.clearStacks();
      // @TypeSafeStudies
      // Clears OHIF.viewer.Studies collection
      //OHIF.viewer.Studies.removeAll();
      // @TypeSafeStudies
      // Clears OHIF.viewer.StudyMetadataList collection
      //OHIF.viewer.StudyMetadataList.removeAll();
    }
  }]);

  return ViewerMain;
}(react["Component"]);

ViewerMain_defineProperty(ViewerMain_ViewerMain, "propTypes", {
  activeViewportIndex: prop_types_default.a.number.isRequired,
  studies: prop_types_default.a.array,
  viewportSpecificData: prop_types_default.a.object.isRequired,
  layout: prop_types_default.a.object.isRequired,
  setViewportSpecificData: prop_types_default.a.func.isRequired,
  clearViewportSpecificData: prop_types_default.a.func.isRequired
});

/* harmony default export */ var connectedComponents_ViewerMain_0 = (ViewerMain_ViewerMain);
// CONCATENATED MODULE: ./connectedComponents/ConnectedViewerMain.js



var ConnectedViewerMain_OHIF$redux$actions = core_src["a" /* default */].redux.actions,
    _setViewportSpecificData = ConnectedViewerMain_OHIF$redux$actions.setViewportSpecificData,
    _clearViewportSpecificData = ConnectedViewerMain_OHIF$redux$actions.clearViewportSpecificData;

var ConnectedViewerMain_mapStateToProps = function mapStateToProps(state) {
  var _state$viewports = state.viewports,
      activeViewportIndex = _state$viewports.activeViewportIndex,
      layout = _state$viewports.layout,
      viewportSpecificData = _state$viewports.viewportSpecificData;
  return {
    activeViewportIndex: activeViewportIndex,
    layout: layout,
    viewportSpecificData: viewportSpecificData,
    viewports: state.viewports
  };
};

var ConnectedViewerMain_mapDispatchToProps = function mapDispatchToProps(dispatch) {
  return {
    setViewportSpecificData: function setViewportSpecificData(viewportIndex, data) {
      dispatch(_setViewportSpecificData(viewportIndex, data));
    },
    clearViewportSpecificData: function clearViewportSpecificData() {
      dispatch(_clearViewportSpecificData());
    }
  };
};

var ConnectedViewerMain = Object(es["b" /* connect */])(ConnectedViewerMain_mapStateToProps, ConnectedViewerMain_mapDispatchToProps)(connectedComponents_ViewerMain_0);
/* harmony default export */ var connectedComponents_ConnectedViewerMain = (ConnectedViewerMain);
// EXTERNAL MODULE: ./components/SidePanel.css
var components_SidePanel = __webpack_require__(1206);

// CONCATENATED MODULE: ./components/SidePanel.js





var SidePanel_SidePanel = function SidePanel(_ref) {
  var from = _ref.from,
      isOpen = _ref.isOpen,
      children = _ref.children,
      width = _ref.width;
  var fromSideClass = from === 'right' ? 'from-right' : 'from-left';
  var styles = width ? {
    maxWidth: width,
    marginRight: isOpen ? '0' : Number.parseInt(width) * -1
  } : {};
  return react_default.a.createElement("section", {
    style: styles,
    className: classnames_default()('sidepanel', fromSideClass, {
      'is-open': isOpen
    })
  }, children);
};

SidePanel_SidePanel.propTypes = {
  from: prop_types_default.a.string.isRequired,
  isOpen: prop_types_default.a.bool.isRequired,
  children: prop_types_default.a.node,
  width: prop_types_default.a.string
};
/* harmony default export */ var components_SidePanel_0 = (SidePanel_SidePanel);
// EXTERNAL MODULE: ./components/ErrorBoundaryDialog/ErrorBoundaryDialog.css
var ErrorBoundaryDialog_ErrorBoundaryDialog = __webpack_require__(1207);

// CONCATENATED MODULE: ./components/ErrorBoundaryDialog/ErrorBoundaryDialog.js
function ErrorBoundaryDialog_slicedToArray(arr, i) { return ErrorBoundaryDialog_arrayWithHoles(arr) || ErrorBoundaryDialog_iterableToArrayLimit(arr, i) || ErrorBoundaryDialog_nonIterableRest(); }

function ErrorBoundaryDialog_nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function ErrorBoundaryDialog_iterableToArrayLimit(arr, i) { if (!(Symbol.iterator in Object(arr) || Object.prototype.toString.call(arr) === "[object Arguments]")) { return; } var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function ErrorBoundaryDialog_arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }







var UIModalService = App["e" /* servicesManager */].services.UIModalService;

var ErrorBoundaryDialog_ErrorBoundaryDialog_ErrorBoundaryDialog = function ErrorBoundaryDialog(_ref) {
  var context = _ref.context,
      children = _ref.children;

  var handleOnError = function handleOnError(error, componentStack) {
    var ErrorDialog = function ErrorDialog() {
      var _useState = Object(react["useState"])(false),
          _useState2 = ErrorBoundaryDialog_slicedToArray(_useState, 2),
          open = _useState2[0],
          setOpen = _useState2[1];

      return react_default.a.createElement("div", {
        className: "ErrorFallback",
        role: "alert"
      }, react_default.a.createElement("div", {
        className: "ErrorBoundaryDialog"
      }, react_default.a.createElement("h3", {
        className: "ErrorBoundaryDialogTitle"
      }, context, ": ", react_default.a.createElement("span", null, error.message))), react_default.a.createElement("button", {
        className: "btn btn-primary btn-sm ErrorBoundaryDialogButton",
        onClick: function onClick() {
          return setOpen(function (s) {
            return !s;
          });
        }
      }, react_default.a.createElement(src["k" /* Icon */], {
        name: "chevron-down",
        className: classnames_default()('ErrorBoundaryDialogIcon', {
          opened: open
        })
      }), "Stack Trace"), open && react_default.a.createElement("pre", null, componentStack));
    };

    UIModalService.show({
      content: ErrorDialog,
      title: "Something went wrong in ".concat(context)
    });
  };

  var fallbackComponent = function fallbackComponent() {
    return react_default.a.createElement("div", {
      className: "ErrorFallback",
      role: "alert"
    }, react_default.a.createElement("p", null, "Error rendering ", context, ". ", react_default.a.createElement("br", null), " Check the browser console for more details."));
  };

  return react_default.a.createElement(src["g" /* ErrorBoundary */], {
    fallbackComponent: fallbackComponent,
    context: context,
    onError: handleOnError
  }, children);
};

ErrorBoundaryDialog_ErrorBoundaryDialog_ErrorBoundaryDialog.propTypes = {
  context: prop_types_default.a.string.isRequired,
  children: prop_types_default.a.node.isRequired
};
/* harmony default export */ var components_ErrorBoundaryDialog_ErrorBoundaryDialog = (ErrorBoundaryDialog_ErrorBoundaryDialog_ErrorBoundaryDialog);
// CONCATENATED MODULE: ./components/ErrorBoundaryDialog/index.js

/* harmony default export */ var components_ErrorBoundaryDialog = (components_ErrorBoundaryDialog_ErrorBoundaryDialog);
// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/core/src/enums.js
var enums = __webpack_require__(96);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/dcmjs/build/dcmjs.es.js
var dcmjs_es = __webpack_require__(35);

// EXTERNAL MODULE: ./context/WhiteLabelingContext.js
var WhiteLabelingContext = __webpack_require__(274);

// EXTERNAL MODULE: ./context/UserManagerContext.js
var UserManagerContext = __webpack_require__(305);

// EXTERNAL MODULE: ./connectedComponents/Viewer.css
var connectedComponents_Viewer = __webpack_require__(1208);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/stream-browserify/index.js
var stream_browserify = __webpack_require__(723);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/cornerstone-wado-image-loader/dist/cornerstoneWADOImageLoader.min.js
var cornerstoneWADOImageLoader_min = __webpack_require__(63);

// CONCATENATED MODULE: ./connectedComponents/Viewer.js
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function Viewer_typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { Viewer_typeof = function _typeof(obj) { return typeof obj; }; } else { Viewer_typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return Viewer_typeof(obj); }

function Viewer_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function Viewer_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function Viewer_createClass(Constructor, protoProps, staticProps) { if (protoProps) Viewer_defineProperties(Constructor.prototype, protoProps); if (staticProps) Viewer_defineProperties(Constructor, staticProps); return Constructor; }

function Viewer_possibleConstructorReturn(self, call) { if (call && (Viewer_typeof(call) === "object" || typeof call === "function")) { return call; } return Viewer_assertThisInitialized(self); }

function Viewer_getPrototypeOf(o) { Viewer_getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return Viewer_getPrototypeOf(o); }

function Viewer_assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function Viewer_inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) Viewer_setPrototypeOf(subClass, superClass); }

function Viewer_setPrototypeOf(o, p) { Viewer_setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return Viewer_setPrototypeOf(o, p); }

function Viewer_defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
















 // Contexts








var Viewer_Viewer =
/*#__PURE__*/
function (_Component) {
  Viewer_inherits(Viewer, _Component);

  function Viewer(props) {
    var _this;

    Viewer_classCallCheck(this, Viewer);

    _this = Viewer_possibleConstructorReturn(this, Viewer_getPrototypeOf(Viewer).call(this, props));

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "state", {
      isLeftSidePanelOpen: true,
      isRightSidePanelOpen: false,
      selectedRightSidePanel: '',
      selectedLeftSidePanel: 'studies',
      // TODO: Don't hardcode this
      thumbnails: []
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "retrieveTimepoints", function (filter) {
      core_src["a" /* default */].log.info('retrieveTimepoints'); // Get the earliest and latest study date

      var earliestDate = new Date().toISOString();
      var latestDate = new Date().toISOString();

      if (_this.props.studies) {
        latestDate = new Date('1000-01-01').toISOString();

        _this.props.studies.forEach(function (study) {
          var StudyDate = moment_default()(study.StudyDate, 'YYYYMMDD').toISOString();

          if (StudyDate < earliestDate) {
            earliestDate = StudyDate;
          }

          if (StudyDate > latestDate) {
            latestDate = StudyDate;
          }
        });
      } // Return a generic timepoint


      return Promise.resolve([{
        timepointType: 'baseline',
        timepointId: 'TimepointId',
        studyInstanceUIDs: _this.props.studyInstanceUIDs,
        PatientID: filter.PatientID,
        earliestDate: earliestDate,
        latestDate: latestDate,
        isLocked: false
      }]);
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "storeTimepoints", function (timepointData) {
      core_src["a" /* default */].log.info('storeTimepoints');
      return Promise.resolve();
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "updateTimepoint", function (timepointData, query) {
      core_src["a" /* default */].log.info('updateTimepoint');
      return Promise.resolve();
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "removeTimepoint", function (timepointId) {
      core_src["a" /* default */].log.info('removeTimepoint');
      return Promise.resolve();
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "disassociateStudy", function (timepointIds, StudyInstanceUID) {
      core_src["a" /* default */].log.info('disassociateStudy');
      return Promise.resolve();
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "onTimepointsUpdated", function (timepoints) {
      if (_this.props.onTimepointsUpdated) {
        _this.props.onTimepointsUpdated(timepoints);
      }
    });

    Viewer_defineProperty(Viewer_assertThisInitialized(_this), "onMeasurementsUpdated", function (measurements) {
      if (_this.props.onMeasurementsUpdated) {
        _this.props.onMeasurementsUpdated(measurements);
      }
    });

    var activeServer = _this.props.activeServer;
    var server = Object.assign({}, activeServer);
    core_src["a" /* default */].measurements.MeasurementApi.setConfiguration({
      dataExchange: {
        retrieve: DICOMSR["a" /* default */].retrieveMeasurements,
        store: DICOMSR["a" /* default */].storeMeasurements
      },
      server: server
    });
    core_src["a" /* default */].measurements.TimepointApi.setConfiguration({
      dataExchange: {
        retrieve: _this.retrieveTimepoints,
        store: _this.storeTimepoints,
        remove: _this.removeTimepoint,
        update: _this.updateTimepoint,
        disassociate: _this.disassociateStudy
      }
    });
    _this._getActiveViewport = _this._getActiveViewport.bind(Viewer_assertThisInitialized(_this));
    return _this;
  }

  Viewer_createClass(Viewer, [{
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      if (this.props.dialog) {
        this.props.dialog.dismissAll();
      }
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      var _this$props = this.props,
          studies = _this$props.studies,
          isStudyLoaded = _this$props.isStudyLoaded;
      var _OHIF$measurements = core_src["a" /* default */].measurements,
          TimepointApi = _OHIF$measurements.TimepointApi,
          MeasurementApi = _OHIF$measurements.MeasurementApi;
      var currentTimepointId = 'TimepointId';
      var timepointApi = new TimepointApi(currentTimepointId, {
        onTimepointsUpdated: this.onTimepointsUpdated
      });
      var measurementApi = new MeasurementApi(timepointApi, {
        onMeasurementsUpdated: this.onMeasurementsUpdated
      });
      this.currentTimepointId = currentTimepointId;
      this.timepointApi = timepointApi;
      this.measurementApi = measurementApi;

      if (studies) {
        var PatientID = studies[0] && studies[0].PatientID;
        timepointApi.retrieveTimepoints({
          PatientID: PatientID
        });

        if (isStudyLoaded) {
          this.measurementApi.retrieveMeasurements(PatientID, [currentTimepointId]);
        }

        var activeViewport = this.props.viewports[this.props.activeViewportIndex];
        var activeDisplaySetInstanceUID = activeViewport ? activeViewport.displaySetInstanceUID : undefined;
        this.setState({
          thumbnails: _mapStudiesToThumbnails(studies, activeDisplaySetInstanceUID)
        });
      }
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate(prevProps) {
      var _this$props2 = this.props,
          studies = _this$props2.studies,
          isStudyLoaded = _this$props2.isStudyLoaded,
          activeViewportIndex = _this$props2.activeViewportIndex,
          viewports = _this$props2.viewports;
      var activeViewport = viewports[activeViewportIndex];
      var activeDisplaySetInstanceUID = activeViewport ? activeViewport.displaySetInstanceUID : undefined;
      var prevActiveViewport = prevProps.viewports[prevProps.activeViewportIndex];
      var prevActiveDisplaySetInstanceUID = prevActiveViewport ? prevActiveViewport.displaySetInstanceUID : undefined;

      if (studies !== prevProps.studies || activeViewportIndex !== prevProps.activeViewportIndex || activeDisplaySetInstanceUID !== prevActiveDisplaySetInstanceUID) {
        this.setState({
          thumbnails: _mapStudiesToThumbnails(studies, activeDisplaySetInstanceUID)
        });
      }

      if (isStudyLoaded && isStudyLoaded !== prevProps.isStudyLoaded) {
        var PatientID = studies[0] && studies[0].PatientID;
        var currentTimepointId = this.currentTimepointId;
        this.timepointApi.retrieveTimepoints({
          PatientID: PatientID
        });
        this.measurementApi.retrieveMeasurements(PatientID, [currentTimepointId]);
      }
    }
  }, {
    key: "_getActiveViewport",
    value: function _getActiveViewport() {
      return this.props.viewports[this.props.activeViewportIndex];
    }
  }, {
    key: "render",
    value: function render() {
      var _this2 = this;

      var VisiblePanelLeft, VisiblePanelRight;
      var panelExtensions = App["c" /* extensionManager */].modules[MODULE_TYPES["a" /* default */].PANEL];
      panelExtensions.forEach(function (panelExt) {
        panelExt.module.components.forEach(function (comp) {
          if (comp.id === _this2.state.selectedRightSidePanel) {
            VisiblePanelRight = comp.component;
          } else if (comp.id === _this2.state.selectedLeftSidePanel) {
            VisiblePanelLeft = comp.component;
          }
        });
      });
      return react_default.a.createElement(react_default.a.Fragment, null, react_default.a.createElement(WhiteLabelingContext["a" /* default */].Consumer, null, function (whiteLabeling) {
        return react_default.a.createElement(UserManagerContext["a" /* default */].Consumer, null, function (userManager) {
          return react_default.a.createElement(AppContext["c" /* default */].Consumer, null, function (appContext) {
            return react_default.a.createElement(ConnectedHeader["a" /* default */], {
              linkText: appContext.appConfig.showStudyList ? 'Study List' : undefined,
              linkPath: appContext.appConfig.showStudyList ? '/' : undefined,
              userManager: userManager
            }, whiteLabeling && whiteLabeling.createLogoComponentFn && whiteLabeling.createLogoComponentFn(react_default.a));
          });
        });
      }), react_default.a.createElement(components_ErrorBoundaryDialog, {
        context: "ToolbarRow"
      }, react_default.a.createElement(connectedComponents_ToolbarRow_0, {
        activeViewport: this.props.viewports[this.props.activeViewportIndex],
        isDerivedDisplaySetsLoaded: this.props.isDerivedDisplaySetsLoaded,
        isLeftSidePanelOpen: this.state.isLeftSidePanelOpen,
        isRightSidePanelOpen: this.state.isRightSidePanelOpen,
        selectedLeftSidePanel: this.state.isLeftSidePanelOpen ? this.state.selectedLeftSidePanel : '',
        selectedRightSidePanel: this.state.isRightSidePanelOpen ? this.state.selectedRightSidePanel : '',
        handleSidePanelChange: function handleSidePanelChange(side, selectedPanel) {
          var sideClicked = side && side[0].toUpperCase() + side.slice(1);
          var openKey = "is".concat(sideClicked, "SidePanelOpen");
          var selectedKey = "selected".concat(sideClicked, "SidePanel");
          var updatedState = Object.assign({}, _this2.state);
          var isOpen = updatedState[openKey];
          var prevSelectedPanel = updatedState[selectedKey]; // RoundedButtonGroup returns `null` if selected button is clicked

          var isSameSelectedPanel = prevSelectedPanel === selectedPanel || selectedPanel === null;
          updatedState[selectedKey] = selectedPanel || prevSelectedPanel;
          var isClosedOrShouldClose = !isOpen || isSameSelectedPanel;

          if (isClosedOrShouldClose) {
            updatedState[openKey] = !updatedState[openKey];
          }

          _this2.setState(updatedState);
        },
        studies: this.props.studies
      })), react_default.a.createElement("div", {
        className: "FlexboxLayout"
      }, react_default.a.createElement(components_ErrorBoundaryDialog, {
        context: "LeftSidePanel"
      }, react_default.a.createElement(components_SidePanel_0, {
        from: "left",
        isOpen: this.state.isLeftSidePanelOpen
      }, VisiblePanelLeft ? react_default.a.createElement(VisiblePanelLeft, {
        viewports: this.props.viewports,
        studies: this.props.studies,
        activeIndex: this.props.activeViewportIndex
      }) : react_default.a.createElement(connectedComponents_ConnectedStudyBrowser, {
        studies: this.state.thumbnails,
        studyMetadata: this.props.studies
      }))), react_default.a.createElement("div", {
        className: classnames_default()('main-content')
      }, react_default.a.createElement(components_ErrorBoundaryDialog, {
        context: "ViewerMain"
      }, react_default.a.createElement(connectedComponents_ConnectedViewerMain, {
        studies: this.props.studies,
        isStudyLoaded: this.props.isStudyLoaded
      }))), react_default.a.createElement(components_ErrorBoundaryDialog, {
        context: "RightSidePanel"
      }, react_default.a.createElement(components_SidePanel_0, {
        from: "right",
        isOpen: this.state.isRightSidePanelOpen
      }, VisiblePanelRight && react_default.a.createElement(VisiblePanelRight, {
        isOpen: this.state.isRightSidePanelOpen,
        viewports: this.props.viewports,
        studies: this.props.studies,
        activeIndex: this.props.activeViewportIndex,
        activeViewport: this.props.viewports[this.props.activeViewportIndex],
        getActiveViewport: this._getActiveViewport
      })))));
    }
  }]);

  return Viewer;
}(react["Component"]);

Viewer_defineProperty(Viewer_Viewer, "propTypes", {
  studies: prop_types_default.a.arrayOf(prop_types_default.a.shape({
    StudyInstanceUID: prop_types_default.a.string.isRequired,
    StudyDate: prop_types_default.a.string,
    PatientID: prop_types_default.a.string,
    displaySets: prop_types_default.a.arrayOf(prop_types_default.a.shape({
      displaySetInstanceUID: prop_types_default.a.string.isRequired,
      SeriesDescription: prop_types_default.a.string,
      SeriesNumber: prop_types_default.a.number,
      InstanceNumber: prop_types_default.a.number,
      numImageFrames: prop_types_default.a.number,
      Modality: prop_types_default.a.string.isRequired,
      images: prop_types_default.a.arrayOf(prop_types_default.a.shape({
        getImageId: prop_types_default.a.func.isRequired
      }))
    }))
  })),
  studyInstanceUIDs: prop_types_default.a.array,
  activeServer: prop_types_default.a.shape({
    type: prop_types_default.a.string,
    wadoRoot: prop_types_default.a.string
  }),
  onTimepointsUpdated: prop_types_default.a.func,
  onMeasurementsUpdated: prop_types_default.a.func,
  // window.store.getState().viewports.viewportSpecificData
  viewports: prop_types_default.a.object.isRequired,
  // window.store.getState().viewports.activeViewportIndex
  activeViewportIndex: prop_types_default.a.number.isRequired,
  isStudyLoaded: prop_types_default.a.bool,
  dialog: prop_types_default.a.object
});

/* harmony default export */ var connectedComponents_Viewer_0 = (Object(src["T" /* withDialog */])(Viewer_Viewer));
/**
 * Async function to check if there are any inconsistences in the series.
 *
 * For segmentation checks that the geometry is consistent with the source images:
 * 1) no frames out of plane;
 * 2) have the same width and height.
 *
 * For reconstructable 3D volume:
 * 1) Is series multiframe?
 * 2) Do the frames have different dimensions/number of components/orientations?
 * 3) Has the series any missing frames or irregular spacing?
 * 4) Is the series 4D?
 *
 * If not reconstructable, MPR is disabled.
 * The actual computations are done in isDisplaySetReconstructable.
 *
 * @param {*object} displaySet
 * @returns {[string]} an array of strings containing the warnings
 */

var _checkForSeriesInconsistencesWarnings =
/*#__PURE__*/
function () {
  var _ref = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee(displaySet, studies) {
    var inconsistencyWarnings, segMetadata, _displaySet$getSource, referencedDisplaySet, imageIds, _loop2, i, groupsLen, _ret, warningMessage;

    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            if (!displaySet.inconsistencyWarnings) {
              _context.next = 2;
              break;
            }

            return _context.abrupt("return", displaySet.inconsistencyWarnings);

          case 2:
            inconsistencyWarnings = [];

            if (!(displaySet.Modality !== 'SEG')) {
              _context.next = 8;
              break;
            }

            if (displaySet.reconstructionIssues && displaySet.reconstructionIssues.length !== 0) {
              displaySet.reconstructionIssues.forEach(function (warning) {
                switch (warning) {
                  case enums["a" /* ReconstructionIssues */].DATASET_4D:
                    inconsistencyWarnings.push('The dataset is 4D.');
                    break;

                  case enums["a" /* ReconstructionIssues */].VARYING_IMAGESDIMENSIONS:
                    inconsistencyWarnings.push('The dataset frames have different dimensions (rows, columns).');
                    break;

                  case enums["a" /* ReconstructionIssues */].VARYING_IMAGESCOMPONENTS:
                    inconsistencyWarnings.push('The dataset frames have different components (Sample per pixel).');
                    break;

                  case enums["a" /* ReconstructionIssues */].VARYING_IMAGESORIENTATION:
                    inconsistencyWarnings.push('The dataset frames have different orientation.');
                    break;

                  case enums["a" /* ReconstructionIssues */].IRREGULAR_SPACING:
                    inconsistencyWarnings.push('The dataset frames have different pixel spacing.');
                    break;

                  case enums["a" /* ReconstructionIssues */].MULTIFFRAMES:
                    inconsistencyWarnings.push('The dataset is a multiframes.');
                    break;

                  default:
                    break;
                }
              });
              inconsistencyWarnings.push('The datasets is not a reconstructable 3D volume. MPR mode is not available.');
            }

            if (displaySet.missingFrames && (!displaySet.reconstructionIssues || displaySet.reconstructionIssues && !displaySet.reconstructionIssues.find(function (warn) {
              return warn === enums["a" /* ReconstructionIssues */].DATASET_4D;
            }))) {
              inconsistencyWarnings.push('The datasets is missing frames: ' + displaySet.missingFrames + '.');
            }

            _context.next = 33;
            break;

          case 8:
            segMetadata = displaySet.metadata;

            if (segMetadata) {
              _context.next = 12;
              break;
            }

            displaySet.inconsistencyWarnings = inconsistencyWarnings;
            return _context.abrupt("return", inconsistencyWarnings);

          case 12:
            _displaySet$getSource = displaySet.getSourceDisplaySet(studies, false), referencedDisplaySet = _displaySet$getSource.referencedDisplaySet;

            if (referencedDisplaySet) {
              _context.next = 16;
              break;
            }

            displaySet.inconsistencyWarnings = inconsistencyWarnings;
            return _context.abrupt("return", inconsistencyWarnings);

          case 16:
            imageIds = referencedDisplaySet.images.map(function (image) {
              return image.getImageId();
            });

            if (!(!imageIds || imageIds.length === 0)) {
              _context.next = 20;
              break;
            }

            displaySet.inconsistencyWarnings = inconsistencyWarnings;
            return _context.abrupt("return", inconsistencyWarnings);

          case 20:
            _loop2 = function _loop2(i, groupsLen) {
              var PerFrameFunctionalGroups = segMetadata.PerFrameFunctionalGroupsSequence[i];

              if (!PerFrameFunctionalGroups) {
                return "continue";
              }

              var SourceImageSequence = undefined;

              if (segMetadata.SourceImageSequence) {
                SourceImageSequence = segMetadata.SourceImageSequence[i];
              } else if (PerFrameFunctionalGroups.DerivationImageSequence) {
                SourceImageSequence = PerFrameFunctionalGroups.DerivationImageSequence.SourceImageSequence;
              }

              if (!SourceImageSequence) {
                if (inconsistencyWarnings.length === 0) {
                  var _warningMessage = 'The segmentation ' + 'has frames out of plane respect to the source images.';

                  inconsistencyWarnings.push(_warningMessage);
                }

                return "continue";
              }

              var _SourceImageSequence = SourceImageSequence,
                  ReferencedSOPInstanceUID = _SourceImageSequence.ReferencedSOPInstanceUID;
              var imageId = imageIds.find(function (imageId) {
                var sopCommonModule = cornerstone.metaData.get("sopCommonModule", imageId);

                if (!sopCommonModule) {
                  return;
                }

                return sopCommonModule.sopInstanceUID === ReferencedSOPInstanceUID;
              });

              if (!imageId) {
                return "continue";
              }

              var sourceImageMetadata = cornerstone.metaData.get("instance", imageId);

              if (segMetadata.Rows !== sourceImageMetadata.Rows || segMetadata.Columns !== sourceImageMetadata.Columns) {
                var _warningMessage2 = 'The segmentation ' + 'has frames with different geometry ' + 'dimensions (Rows and Columns) respect to the source images.';

                inconsistencyWarnings.push(_warningMessage2);
                return "break";
              }
            };

            i = 0, groupsLen = segMetadata.PerFrameFunctionalGroupsSequence.length;

          case 22:
            if (!(i < groupsLen)) {
              _context.next = 32;
              break;
            }

            _ret = _loop2(i, groupsLen);
            _context.t0 = _ret;
            _context.next = _context.t0 === "continue" ? 27 : _context.t0 === "break" ? 28 : 29;
            break;

          case 27:
            return _context.abrupt("continue", 29);

          case 28:
            return _context.abrupt("break", 32);

          case 29:
            ++i;
            _context.next = 22;
            break;

          case 32:
            if (inconsistencyWarnings.length !== 0) {
              warningMessage = 'The segmentation format is not supported yet. ' + 'The segmentation data (segments) could not be loaded.';
              inconsistencyWarnings.push(warningMessage);
            }

          case 33:
            // cache the warnings
            displaySet.inconsistencyWarnings = inconsistencyWarnings;
            return _context.abrupt("return", inconsistencyWarnings);

          case 35:
          case "end":
            return _context.stop();
        }
      }
    }, _callee);
  }));

  return function _checkForSeriesInconsistencesWarnings(_x, _x2) {
    return _ref.apply(this, arguments);
  };
}();
/**
 * Checks if display set is active, i.e. if the series is currently shown
 * in the active viewport.
 *
 * For data display set, this functions checks if the active
 * display set instance uid in the current active viewport is the same of the
 * thumbnail one.
 *
 * For derived modalities (e.g., SEG and RTSTRUCT), the function gets the
 * reference display set and then checks the reference uid with the active
 * display set instance uid.
 *
 * @param {displaySet} displaySet
 * @param {Study[]} studies
 * @param {string} activeDisplaySetInstanceUID
 * @returns {boolean} is active.
 */


var _isDisplaySetActive = function _isDisplaySetActive(displaySet, studies, activeDisplaySetInstanceUID) {
  var active = false;
  var displaySetInstanceUID = displaySet.displaySetInstanceUID; // TO DO: in the future, we could possibly support new modalities
  // we should have a list of all modalities here, instead of having hard coded checks

  if (displaySet.Modality !== 'SEG' && displaySet.Modality !== 'RTSTRUCT' && displaySet.Modality !== 'RTDOSE') {
    active = activeDisplaySetInstanceUID === displaySetInstanceUID;
  } else if (displaySet.getSourceDisplaySet) {
    if (displaySet.Modality === 'SEG') {
      var _displaySet$getSource2 = displaySet.getSourceDisplaySet(studies, false),
          referencedDisplaySet = _displaySet$getSource2.referencedDisplaySet;

      active = referencedDisplaySet ? activeDisplaySetInstanceUID === referencedDisplaySet.displaySetInstanceUID : false;
    } else {
      var _referencedDisplaySet = displaySet.getSourceDisplaySet(studies, false);

      active = _referencedDisplaySet ? activeDisplaySetInstanceUID === _referencedDisplaySet.displaySetInstanceUID : false;
    }
  }

  return active;
};
/**
 * What types are these? Why do we have "mapping" dropped in here instead of in
 * a mapping layer?
 *
 * TODO[react]:
 * - Add showStackLoadingProgressBar option
 *
 * @param {Study[]} studies
 * @param {string} activeDisplaySetInstanceUID
 */


var _mapStudiesToThumbnails = function _mapStudiesToThumbnails(studies, activeDisplaySetInstanceUID) {
  return studies.map(function (study) {
    var StudyInstanceUID = study.StudyInstanceUID;
    var thumbnails = study.displaySets.map(function (displaySet) {
      var displaySetInstanceUID = displaySet.displaySetInstanceUID,
          SeriesDescription = displaySet.SeriesDescription,
          InstanceNumber = displaySet.InstanceNumber,
          numImageFrames = displaySet.numImageFrames,
          SeriesNumber = displaySet.SeriesNumber;
      var imageId;
      var altImageText;

      if (displaySet.Modality && displaySet.Modality === 'SEG') {
        // TODO: We want to replace this with a thumbnail showing
        // the segmentation map on the image, but this is easier
        // and better than what we have right now.
        altImageText = 'SEG';
      } else if (displaySet.images && displaySet.images.length) {
        var imageIndex = Math.floor(displaySet.images.length / 2);
        imageId = displaySet.images[imageIndex].getImageId();
      } else {
        altImageText = displaySet.Modality ? displaySet.Modality : 'UN';
      }

      var hasWarnings = _checkForSeriesInconsistencesWarnings(displaySet, studies);

      var active = _isDisplaySetActive(displaySet, studies, activeDisplaySetInstanceUID);

      return {
        active: active,
        imageId: imageId,
        altImageText: altImageText,
        displaySetInstanceUID: displaySetInstanceUID,
        SeriesDescription: SeriesDescription,
        InstanceNumber: InstanceNumber,
        numImageFrames: numImageFrames,
        SeriesNumber: SeriesNumber,
        hasWarnings: hasWarnings
      };
    });
    return {
      StudyInstanceUID: StudyInstanceUID,
      thumbnails: thumbnails
    };
  });
};
// CONCATENATED MODULE: ./connectedComponents/ConnectedViewer.js



var ConnectedViewer_OHIF$redux$actions = core_src["a" /* default */].redux.actions,
    setTimepoints = ConnectedViewer_OHIF$redux$actions.setTimepoints,
    setMeasurements = ConnectedViewer_OHIF$redux$actions.setMeasurements;

var getActiveServer = function getActiveServer(servers) {
  var isActive = function isActive(a) {
    return a.active === true;
  };

  return servers.servers.find(isActive);
};

var ConnectedViewer_mapStateToProps = function mapStateToProps(state) {
  var viewports = state.viewports,
      servers = state.servers;
  return {
    viewports: viewports.viewportSpecificData,
    activeViewportIndex: viewports.activeViewportIndex,
    activeServer: getActiveServer(servers)
  };
};

var ConnectedViewer_mapDispatchToProps = function mapDispatchToProps(dispatch) {
  return {
    onTimepointsUpdated: function onTimepointsUpdated(timepoints) {
      dispatch(setTimepoints(timepoints));
    },
    onMeasurementsUpdated: function onMeasurementsUpdated(measurements) {
      dispatch(setMeasurements(measurements));
    }
  };
};

var ConnectedViewer = Object(es["b" /* connect */])(ConnectedViewer_mapStateToProps, ConnectedViewer_mapDispatchToProps)(connectedComponents_Viewer_0);
/* harmony default export */ var connectedComponents_ConnectedViewer = __webpack_exports__["a"] = (ConnectedViewer);

/***/ }),

/***/ 1201:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1202:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1203:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1204:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1205:
/***/ (function(module, exports) {

/**
 *
 *
 * @returns
 */
function EmptyViewport() {
  return React.createElement("div", {
    className: "empty-viewport"
  }, React.createElement("p", null, "Please drag a stack here to view images."));
}

/***/ }),

/***/ 1206:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1207:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1208:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ })

}]);