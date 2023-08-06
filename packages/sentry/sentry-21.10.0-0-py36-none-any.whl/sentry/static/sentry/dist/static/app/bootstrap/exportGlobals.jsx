Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const ReactRouter = (0, tslib_1.__importStar)(require("react-router"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const plugins_1 = (0, tslib_1.__importDefault)(require("app/plugins"));
const globals = {
    // The following globals are used in sentry-plugins webpack externals
    // configuration.
    PropTypes: prop_types_1.default,
    React,
    Reflux: reflux_1.default,
    Sentry,
    moment: moment_1.default,
    Router: ReactRouter,
    ReactDOM: {
        findDOMNode: react_dom_1.default.findDOMNode,
        render: react_dom_1.default.render,
    },
    // django templates make use of these globals
    SentryApp: {},
};
// The SentryApp global contains exported app modules for use in javascript
// modules that are not compiled with the sentry bundle.
const SentryApp = {
    // The following components are used in sentry-plugins.
    Form: require('app/components/forms/form').default,
    FormState: require('app/components/forms/index').FormState,
    LoadingIndicator: require('app/components/loadingIndicator').default,
    plugins: {
        add: plugins_1.default.add,
        addContext: plugins_1.default.addContext,
        BasePlugin: plugins_1.default.BasePlugin,
        DefaultIssuePlugin: plugins_1.default.DefaultIssuePlugin,
    },
    // The following components are used in legacy django HTML views
    ConfigStore: require('app/stores/configStore').default,
    HookStore: require('app/stores/hookStore').default,
    Modal: require('app/actionCreators/modal'),
    getModalPortal: require('app/utils/getModalPortal').default,
};
globals.SentryApp = SentryApp;
Object.keys(globals).forEach(name => (window[name] = globals[name]));
exports.default = globals;
//# sourceMappingURL=exportGlobals.jsx.map