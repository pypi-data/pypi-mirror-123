(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[13],{

/***/ 1194:
/***/ (function(module, exports, __webpack_require__) {

// extracted by extract-css-chunks-webpack-plugin

/***/ }),

/***/ 1231:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react/index.js
var react = __webpack_require__(0);
var react_default = /*#__PURE__*/__webpack_require__.n(react);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/prop-types/index.js
var prop_types = __webpack_require__(1);
var prop_types_default = /*#__PURE__*/__webpack_require__.n(prop_types);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/cornerstone-core/dist/cornerstone.js
var dist_cornerstone = __webpack_require__(9);
var cornerstone_default = /*#__PURE__*/__webpack_require__.n(dist_cornerstone);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/extensions/cornerstone/src/components/OHIFCornerstoneViewportOverlay.css
var components_OHIFCornerstoneViewportOverlay = __webpack_require__(1194);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/moment/moment.js
var moment = __webpack_require__(7);
var moment_default = /*#__PURE__*/__webpack_require__.n(moment);

// CONCATENATED MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/extensions/cornerstone/src/utils/formatStudy.js

/**
 * Checks if value is valid.
 *
 * @param {number} value
 * @returns {boolean} is valid.
 */

function isValidNumber(value) {
  return typeof value === 'number' && !isNaN(value);
}
/**
 * Formats number precision.
 *
 * @param {number} number
 * @param {number} precision
 * @returns {number} formatted number.
 */


function formatNumberPrecision(number, precision) {
  if (number !== null) {
    return parseFloat(number).toFixed(precision);
  }
}
/**
 * Formats DICOM date.
 *
 * @param {string} date
 * @param {string} strFormat
 * @returns {string} formatted date.
 */


function formatDICOMDate(date) {
  var strFormat = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'MMM D, YYYY';
  return moment_default()(date, 'YYYYMMDD').format(strFormat);
}
/**
 *    DICOM Time is stored as HHmmss.SSS, where:
 *      HH 24 hour time:
 *        m mm        0..59   Minutes
 *        s ss        0..59   Seconds
 *        S SS SSS    0..999  Fractional seconds
 *
 *        Goal: '24:12:12'
 *
 * @param {*} time
 * @param {string} strFormat
 * @returns {string} formatted name.
 */


function formatDICOMTime(time) {
  var strFormat = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'HH:mm:ss';
  return moment_default()(time, 'HH:mm:ss').format(strFormat);
}
/**
 * Formats a patient name for display purposes
 *
 * @param {string} name
 * @returns {string} formatted name.
 */


function formatPN(name) {
  if (!name) {
    return;
  } // Convert the first ^ to a ', '. String.replace() only affects
  // the first appearance of the character.


  var commaBetweenFirstAndLast = name.replace('^', ', '); // Replace any remaining '^' characters with spaces

  var cleaned = commaBetweenFirstAndLast.replace(/\^/g, ' '); // Trim any extraneous whitespace

  return cleaned.trim();
}
/**
 * Gets compression type
 *
 * @param {number} imageId
 * @returns {string} comrpession type.
 */


function getCompression(imageId) {
  var generalImageModule = cornerstone.metaData.get('generalImageModule', imageId) || {};
  var lossyImageCompression = generalImageModule.lossyImageCompression,
      lossyImageCompressionRatio = generalImageModule.lossyImageCompressionRatio,
      lossyImageCompressionMethod = generalImageModule.lossyImageCompressionMethod;

  if (lossyImageCompression === '01' && lossyImageCompressionRatio !== '') {
    var compressionMethod = lossyImageCompressionMethod || 'Lossy: ';
    var compressionRatio = formatNumberPrecision(lossyImageCompressionRatio, 2);
    return compressionMethod + compressionRatio + ' : 1';
  }

  return 'Lossless / Uncompressed';
}


// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/classnames/index.js
var classnames = __webpack_require__(18);
var classnames_default = /*#__PURE__*/__webpack_require__.n(classnames);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/ui/src/elements/Icon/index.js + 2 modules
var Icon = __webpack_require__(20);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/ui/src/components/tooltip/index.js + 1 modules
var tooltip = __webpack_require__(92);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/ui/src/components/overlayTrigger/index.js + 4 modules
var overlayTrigger = __webpack_require__(85);

// CONCATENATED MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/extensions/cornerstone/src/components/OHIFCornerstoneViewportOverlay.js
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }












var OHIFCornerstoneViewportOverlay_OHIFCornerstoneViewportOverlay =
/*#__PURE__*/
function (_PureComponent) {
  _inherits(OHIFCornerstoneViewportOverlay, _PureComponent);

  function OHIFCornerstoneViewportOverlay() {
    _classCallCheck(this, OHIFCornerstoneViewportOverlay);

    return _possibleConstructorReturn(this, _getPrototypeOf(OHIFCornerstoneViewportOverlay).apply(this, arguments));
  }

  _createClass(OHIFCornerstoneViewportOverlay, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          imageId = _this$props.imageId,
          scale = _this$props.scale,
          windowWidth = _this$props.windowWidth,
          windowCenter = _this$props.windowCenter,
          inconsistencyWarnings = _this$props.inconsistencyWarnings;

      if (!imageId) {
        return null;
      }

      var zoomPercentage = formatNumberPrecision(scale * 100, 0);
      var seriesMetadata = cornerstone_default.a.metaData.get('generalSeriesModule', imageId) || {};
      var imagePlaneModule = cornerstone_default.a.metaData.get('imagePlaneModule', imageId) || {};
      var rows = imagePlaneModule.rows,
          columns = imagePlaneModule.columns,
          sliceThickness = imagePlaneModule.sliceThickness,
          sliceLocation = imagePlaneModule.sliceLocation;
      var seriesNumber = seriesMetadata.seriesNumber,
          seriesDescription = seriesMetadata.seriesDescription;
      var generalStudyModule = cornerstone_default.a.metaData.get('generalStudyModule', imageId) || {};
      var studyDate = generalStudyModule.studyDate,
          studyTime = generalStudyModule.studyTime,
          studyDescription = generalStudyModule.studyDescription;
      var patientModule = cornerstone_default.a.metaData.get('patientModule', imageId) || {};
      var patientId = patientModule.patientId,
          patientName = patientModule.patientName;
      var generalImageModule = cornerstone_default.a.metaData.get('generalImageModule', imageId) || {};
      var instanceNumber = generalImageModule.instanceNumber;
      var cineModule = cornerstone_default.a.metaData.get('cineModule', imageId) || {};
      var frameTime = cineModule.frameTime;
      var frameRate = formatNumberPrecision(1000 / frameTime, 1);
      var compression = getCompression(imageId);
      var wwwc = "W: ".concat(windowWidth.toFixed ? windowWidth.toFixed(0) : windowWidth, " L: ").concat(windowWidth.toFixed ? windowCenter.toFixed(0) : windowCenter);
      var imageDimensions = "".concat(columns, " x ").concat(rows);
      var _this$props2 = this.props,
          imageIndex = _this$props2.imageIndex,
          stackSize = _this$props2.stackSize;
      var inconsistencyWarningsOn = inconsistencyWarnings && inconsistencyWarnings.length !== 0 ? true : false;

      var getWarningContent = function getWarningContent(warningList) {
        if (Array.isArray(warningList)) {
          var listedWarnings = warningList.map(function (warn, index) {
            return react_default.a.createElement("li", {
              key: index
            }, warn);
          });
          return react_default.a.createElement("ol", null, listedWarnings);
        } else {
          return react_default.a.createElement(react_default.a.Fragment, null, warningList);
        }
      };

      var getWarningInfo = function getWarningInfo(seriesNumber, inconsistencyWarnings) {
        return react_default.a.createElement(react_default.a.Fragment, null, inconsistencyWarnings.length != 0 ? react_default.a.createElement(overlayTrigger["a" /* OverlayTrigger */], {
          key: seriesNumber,
          placement: "left",
          overlay: react_default.a.createElement(tooltip["a" /* Tooltip */], {
            placement: "left",
            className: "in tooltip-warning",
            id: "tooltip-left"
          }, react_default.a.createElement("div", {
            className: "warningTitle"
          }, "Series Inconsistencies"), react_default.a.createElement("div", {
            className: "warningContent"
          }, getWarningContent(inconsistencyWarnings)))
        }, react_default.a.createElement("div", {
          className: classnames_default()('warning')
        }, react_default.a.createElement("span", {
          className: "warning-icon"
        }, react_default.a.createElement(Icon["a" /* Icon */], {
          name: "exclamation-triangle"
        })))) : react_default.a.createElement(react_default.a.Fragment, null));
      };

      var normal = react_default.a.createElement(react_default.a.Fragment, null, react_default.a.createElement("div", {
        className: "top-left overlay-element"
      }, react_default.a.createElement("div", null, formatPN(patientName)), react_default.a.createElement("div", null, patientId)), react_default.a.createElement("div", {
        className: "top-right overlay-element"
      }, react_default.a.createElement("div", null, studyDescription), react_default.a.createElement("div", null, formatDICOMDate(studyDate), " ", formatDICOMTime(studyTime))), react_default.a.createElement("div", {
        className: "bottom-right overlay-element"
      }, react_default.a.createElement("div", null, "Zoom: ", zoomPercentage, "%"), react_default.a.createElement("div", null, wwwc), react_default.a.createElement("div", {
        className: "compressionIndicator"
      }, compression)), react_default.a.createElement("div", {
        className: "bottom-left2 warning"
      }, react_default.a.createElement("div", null, inconsistencyWarningsOn ? getWarningInfo(seriesNumber, inconsistencyWarnings) : '')), react_default.a.createElement("div", {
        className: "bottom-left overlay-element"
      }, react_default.a.createElement("div", null, seriesNumber >= 0 ? "Ser: ".concat(seriesNumber) : ''), react_default.a.createElement("div", null, stackSize > 1 ? "Img: ".concat(instanceNumber, " ").concat(imageIndex, "/").concat(stackSize) : ''), react_default.a.createElement("div", null, frameRate >= 0 ? "".concat(formatNumberPrecision(frameRate, 2), " FPS") : '', react_default.a.createElement("div", null, imageDimensions), react_default.a.createElement("div", null, isValidNumber(sliceLocation) ? "Loc: ".concat(formatNumberPrecision(sliceLocation, 2), " mm ") : '', sliceThickness ? "Thick: ".concat(formatNumberPrecision(sliceThickness, 2), " mm") : ''), react_default.a.createElement("div", null, seriesDescription))));
      return react_default.a.createElement("div", {
        className: "OHIFCornerstoneViewportOverlay"
      }, normal);
    }
  }]);

  return OHIFCornerstoneViewportOverlay;
}(react["PureComponent"]);

_defineProperty(OHIFCornerstoneViewportOverlay_OHIFCornerstoneViewportOverlay, "propTypes", {
  scale: prop_types_default.a.number.isRequired,
  windowWidth: prop_types_default.a.oneOfType([prop_types_default.a.number.isRequired, prop_types_default.a.string.isRequired]),
  windowCenter: prop_types_default.a.oneOfType([prop_types_default.a.number.isRequired, prop_types_default.a.string.isRequired]),
  imageId: prop_types_default.a.string.isRequired,
  imageIndex: prop_types_default.a.number.isRequired,
  stackSize: prop_types_default.a.number.isRequired,
  inconsistencyWarnings: prop_types_default.a.array.isRequired
});

/* harmony default export */ var src_components_OHIFCornerstoneViewportOverlay = (OHIFCornerstoneViewportOverlay_OHIFCornerstoneViewportOverlay);
// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react-cornerstone-viewport/dist/index.umd.js
var index_umd = __webpack_require__(1195);
var index_umd_default = /*#__PURE__*/__webpack_require__.n(index_umd);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/platform/core/src/index.js + 33 modules
var src = __webpack_require__(17);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/react-redux/es/index.js + 21 modules
var es = __webpack_require__(66);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/node_modules/lodash.throttle/index.js
var lodash_throttle = __webpack_require__(222);
var lodash_throttle_default = /*#__PURE__*/__webpack_require__.n(lodash_throttle);

// EXTERNAL MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/extensions/cornerstone/src/state.js
var state = __webpack_require__(65);

// CONCATENATED MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/extensions/cornerstone/src/ConnectedCornerstoneViewport.js
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(source, true).forEach(function (key) { ConnectedCornerstoneViewport_defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(source).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function ConnectedCornerstoneViewport_defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }






var _OHIF$redux$actions = src["a" /* default */].redux.actions,
    _setViewportActive = _OHIF$redux$actions.setViewportActive,
    _setViewportSpecificData = _OHIF$redux$actions.setViewportSpecificData;
var _OHIF$measurements$Me = src["a" /* default */].measurements.MeasurementHandlers,
    onAdded = _OHIF$measurements$Me.onAdded,
    onRemoved = _OHIF$measurements$Me.onRemoved,
    onModified = _OHIF$measurements$Me.onModified; // TODO: Transition to enums for the action names so that we can ensure they stay up to date
// everywhere they're used.

var MEASUREMENT_ACTION_MAP = {
  added: onAdded,
  removed: onRemoved,
  modified: lodash_throttle_default()(function (event) {
    return onModified(event);
  }, 300)
};

var mapStateToProps = function mapStateToProps(state, ownProps) {
  var dataFromStore; // TODO: This may not be updated anymore :thinking:

  if (state.extensions && state.extensions.cornerstone) {
    dataFromStore = state.extensions.cornerstone;
  } // If this is the active viewport, enable prefetching.


  var viewportIndex = ownProps.viewportIndex; //.viewportData;

  var isActive = viewportIndex === state.viewports.activeViewportIndex;
  var viewportSpecificData = state.viewports.viewportSpecificData[viewportIndex] || {}; // CINE

  var isPlaying = false;
  var frameRate = 24;

  if (viewportSpecificData && viewportSpecificData.cine) {
    var cine = viewportSpecificData.cine;
    isPlaying = cine.isPlaying === true;
    frameRate = cine.cineFrameRate || frameRate;
  }

  return _objectSpread({
    // layout: state.viewports.layout,
    isActive: isActive
  }, dataFromStore, {
    isStackPrefetchEnabled: isActive,
    isPlaying: isPlaying,
    frameRate: frameRate //stack: viewportSpecificData.stack,
    // viewport: viewportSpecificData.viewport,

  });
};

var ConnectedCornerstoneViewport_mapDispatchToProps = function mapDispatchToProps(dispatch, ownProps) {
  var viewportIndex = ownProps.viewportIndex;
  return {
    setViewportActive: function setViewportActive() {
      dispatch(_setViewportActive(viewportIndex));
    },
    setViewportSpecificData: function setViewportSpecificData(data) {
      dispatch(_setViewportSpecificData(viewportIndex, data));
    },

    /**
     * Our component "enables" the underlying dom element on "componentDidMount"
     * It listens for that event, and then emits the enabledElement. We can grab
     * a reference to it here, to make playing with cornerstone's native methods
     * easier.
     */
    onElementEnabled: function onElementEnabled(event) {
      var enabledElement = event.detail.element;
      Object(state["b" /* setEnabledElement */])(viewportIndex, enabledElement);
      dispatch(_setViewportSpecificData(viewportIndex, {
        // TODO: Hack to make sure our plugin info is available from the outset
        plugin: 'cornerstone'
      }));
    },
    onMeasurementsChanged: function onMeasurementsChanged(event, action) {
      return MEASUREMENT_ACTION_MAP[action](event);
    }
  };
};

var ConnectedCornerstoneViewport = Object(es["b" /* connect */])(mapStateToProps, ConnectedCornerstoneViewport_mapDispatchToProps)(index_umd_default.a);
/* harmony default export */ var src_ConnectedCornerstoneViewport = (ConnectedCornerstoneViewport);
// CONCATENATED MODULE: /home/runner/work/MONAILabel/MONAILabel/plugins/ohif/Viewers/extensions/cornerstone/src/OHIFCornerstoneViewport.js
function OHIFCornerstoneViewport_typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { OHIFCornerstoneViewport_typeof = function _typeof(obj) { return typeof obj; }; } else { OHIFCornerstoneViewport_typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return OHIFCornerstoneViewport_typeof(obj); }

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function OHIFCornerstoneViewport_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function OHIFCornerstoneViewport_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function OHIFCornerstoneViewport_createClass(Constructor, protoProps, staticProps) { if (protoProps) OHIFCornerstoneViewport_defineProperties(Constructor.prototype, protoProps); if (staticProps) OHIFCornerstoneViewport_defineProperties(Constructor, staticProps); return Constructor; }

function OHIFCornerstoneViewport_possibleConstructorReturn(self, call) { if (call && (OHIFCornerstoneViewport_typeof(call) === "object" || typeof call === "function")) { return call; } return OHIFCornerstoneViewport_assertThisInitialized(self); }

function OHIFCornerstoneViewport_getPrototypeOf(o) { OHIFCornerstoneViewport_getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return OHIFCornerstoneViewport_getPrototypeOf(o); }

function OHIFCornerstoneViewport_assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function OHIFCornerstoneViewport_inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) OHIFCornerstoneViewport_setPrototypeOf(subClass, superClass); }

function OHIFCornerstoneViewport_setPrototypeOf(o, p) { OHIFCornerstoneViewport_setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return OHIFCornerstoneViewport_setPrototypeOf(o, p); }

function OHIFCornerstoneViewport_defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }







var StackManager = src["a" /* default */].utils.StackManager;

var OHIFCornerstoneViewport_OHIFCornerstoneViewport =
/*#__PURE__*/
function (_Component) {
  OHIFCornerstoneViewport_inherits(OHIFCornerstoneViewport, _Component);

  function OHIFCornerstoneViewport() {
    var _getPrototypeOf2;

    var _this;

    OHIFCornerstoneViewport_classCallCheck(this, OHIFCornerstoneViewport);

    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    _this = OHIFCornerstoneViewport_possibleConstructorReturn(this, (_getPrototypeOf2 = OHIFCornerstoneViewport_getPrototypeOf(OHIFCornerstoneViewport)).call.apply(_getPrototypeOf2, [this].concat(args)));

    OHIFCornerstoneViewport_defineProperty(OHIFCornerstoneViewport_assertThisInitialized(_this), "state", {
      viewportData: null
    });

    OHIFCornerstoneViewport_defineProperty(OHIFCornerstoneViewport_assertThisInitialized(_this), "getViewportData",
    /*#__PURE__*/
    function () {
      var _ref = _asyncToGenerator(
      /*#__PURE__*/
      regeneratorRuntime.mark(function _callee(studies, StudyInstanceUID, displaySetInstanceUID, SOPInstanceUID, frameIndex) {
        var viewportData, stack;
        return regeneratorRuntime.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                stack = OHIFCornerstoneViewport.getCornerstoneStack(studies, StudyInstanceUID, displaySetInstanceUID, SOPInstanceUID, frameIndex);
                viewportData = {
                  StudyInstanceUID: StudyInstanceUID,
                  displaySetInstanceUID: displaySetInstanceUID,
                  stack: stack
                };
                return _context.abrupt("return", viewportData);

              case 3:
              case "end":
                return _context.stop();
            }
          }
        }, _callee);
      }));

      return function (_x, _x2, _x3, _x4, _x5) {
        return _ref.apply(this, arguments);
      };
    }());

    return _this;
  }

  OHIFCornerstoneViewport_createClass(OHIFCornerstoneViewport, [{
    key: "setStateFromProps",
    value: function setStateFromProps() {
      var _this2 = this;

      var _this$props$viewportD = this.props.viewportData,
          studies = _this$props$viewportD.studies,
          displaySet = _this$props$viewportD.displaySet;
      var StudyInstanceUID = displaySet.StudyInstanceUID,
          displaySetInstanceUID = displaySet.displaySetInstanceUID,
          sopClassUIDs = displaySet.sopClassUIDs,
          SOPInstanceUID = displaySet.SOPInstanceUID,
          frameIndex = displaySet.frameIndex;

      if (!StudyInstanceUID || !displaySetInstanceUID) {
        return;
      }

      if (sopClassUIDs && sopClassUIDs.length > 1) {
        console.warn('More than one SOPClassUID in the same series is not yet supported.');
      }

      this.getViewportData(studies, StudyInstanceUID, displaySetInstanceUID, SOPInstanceUID, frameIndex).then(function (viewportData) {
        _this2.setState({
          viewportData: viewportData
        });
      });
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      this.setStateFromProps();
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate(prevProps) {
      var displaySet = this.props.viewportData.displaySet;
      var prevDisplaySet = prevProps.viewportData.displaySet;

      if (displaySet.displaySetInstanceUID !== prevDisplaySet.displaySetInstanceUID || displaySet.SOPInstanceUID !== prevDisplaySet.SOPInstanceUID || displaySet.frameIndex !== prevDisplaySet.frameIndex) {
        this.setStateFromProps();
      }
    }
  }, {
    key: "render",
    value: function render() {
      var _this3 = this;

      var childrenWithProps = null;

      if (!this.state.viewportData) {
        return null;
      }

      var viewportIndex = this.props.viewportIndex;
      var inconsistencyWarnings = this.props.viewportData.displaySet.inconsistencyWarnings;
      var _this$state$viewportD = this.state.viewportData.stack,
          imageIds = _this$state$viewportD.imageIds,
          currentImageIdIndex = _this$state$viewportD.currentImageIdIndex; // TODO: Does it make more sense to use Context?

      if (this.props.children && this.props.children.length) {
        childrenWithProps = this.props.children.map(function (child, index) {
          return child && react_default.a.cloneElement(child, {
            viewportIndex: _this3.props.viewportIndex,
            key: index
          });
        });
      }

      var newImageHandler = function newImageHandler(_ref2) {
        var currentImageIdIndex = _ref2.currentImageIdIndex,
            sopInstanceUid = _ref2.sopInstanceUid;
        var displaySet = _this3.props.viewportData.displaySet;
        var StudyInstanceUID = displaySet.StudyInstanceUID;

        if (currentImageIdIndex >= 0) {
          _this3.props.onNewImage({
            StudyInstanceUID: StudyInstanceUID,
            SOPInstanceUID: sopInstanceUid,
            frameIndex: currentImageIdIndex,
            activeViewportIndex: viewportIndex
          });
        }
      };

      var warningsOverlay = function warningsOverlay(props) {
        return react_default.a.createElement(src_components_OHIFCornerstoneViewportOverlay, _extends({}, props, {
          inconsistencyWarnings: inconsistencyWarnings
        }));
      };

      return react_default.a.createElement(react_default.a.Fragment, null, react_default.a.createElement(src_ConnectedCornerstoneViewport, _extends({
        viewportIndex: viewportIndex,
        imageIds: imageIds,
        imageIdIndex: currentImageIdIndex,
        onNewImageDebounced: newImageHandler,
        onNewImageDebounceTime: 300,
        viewportOverlayComponent: warningsOverlay // ~~ Connected (From REDUX)
        // frameRate={frameRate}
        // isPlaying={false}
        // isStackPrefetchEnabled={true}
        // onElementEnabled={() => {}}
        // setViewportActive{() => {}}

      }, this.props.customProps)), childrenWithProps);
    }
  }], [{
    key: "init",
    value: function init() {
      console.log('OHIFCornerstoneViewport init()');
    }
  }, {
    key: "destroy",
    value: function destroy() {
      console.log('OHIFCornerstoneViewport destroy()');
      StackManager.clearStacks();
    }
    /**
     * Obtain the CornerstoneTools Stack for the specified display set.
     *
     * @param {Object[]} studies
     * @param {String} StudyInstanceUID
     * @param {String} displaySetInstanceUID
     * @param {String} [SOPInstanceUID]
     * @param {Number} [frameIndex=1]
     * @return {Object} CornerstoneTools Stack
     */

  }, {
    key: "getCornerstoneStack",
    value: function getCornerstoneStack(studies, StudyInstanceUID, displaySetInstanceUID, SOPInstanceUID) {
      var frameIndex = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : 0;

      if (!studies || !studies.length) {
        throw new Error('Studies not provided.');
      }

      if (!StudyInstanceUID) {
        throw new Error('StudyInstanceUID not provided.');
      }

      if (!displaySetInstanceUID) {
        throw new Error('StudyInstanceUID not provided.');
      } // Create shortcut to displaySet


      var study = studies.find(function (study) {
        return study.StudyInstanceUID === StudyInstanceUID;
      });

      if (!study) {
        throw new Error('Study not found.');
      }

      var displaySet = study.displaySets.find(function (set) {
        return set.displaySetInstanceUID === displaySetInstanceUID;
      });

      if (!displaySet) {
        throw new Error('Display Set not found.');
      } // Get stack from Stack Manager


      var storedStack = StackManager.findOrCreateStack(study, displaySet); // Clone the stack here so we don't mutate it

      var stack = Object.assign({}, storedStack);
      stack.currentImageIdIndex = frameIndex;

      if (SOPInstanceUID) {
        var index = stack.imageIds.findIndex(function (imageId) {
          var imageIdSOPInstanceUID = cornerstone_default.a.metaData.get('SOPInstanceUID', imageId);
          return imageIdSOPInstanceUID === SOPInstanceUID;
        });

        if (index > -1) {
          stack.currentImageIdIndex = index;
        } else {
          console.warn('SOPInstanceUID provided was not found in specified DisplaySet');
        }
      }

      return stack;
    }
  }]);

  return OHIFCornerstoneViewport;
}(react["Component"]);

OHIFCornerstoneViewport_defineProperty(OHIFCornerstoneViewport_OHIFCornerstoneViewport, "defaultProps", {
  customProps: {}
});

OHIFCornerstoneViewport_defineProperty(OHIFCornerstoneViewport_OHIFCornerstoneViewport, "propTypes", {
  studies: prop_types_default.a.object,
  displaySet: prop_types_default.a.object,
  viewportIndex: prop_types_default.a.number,
  children: prop_types_default.a.node,
  customProps: prop_types_default.a.object
});

OHIFCornerstoneViewport_defineProperty(OHIFCornerstoneViewport_OHIFCornerstoneViewport, "id", 'OHIFCornerstoneViewport');

/* harmony default export */ var src_OHIFCornerstoneViewport = __webpack_exports__["default"] = (OHIFCornerstoneViewport_OHIFCornerstoneViewport);

/***/ })

}]);