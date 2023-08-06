Object.defineProperty(exports, "__esModule", { value: true });
exports.saveOnBlurUndoMessage = exports.addSuccessMessage = exports.addErrorMessage = exports.addLoadingMessage = exports.addMessage = exports.clearIndicators = exports.removeIndicator = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicatorActions_1 = (0, tslib_1.__importDefault)(require("app/actions/indicatorActions"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
// Removes a single indicator
function removeIndicator(indicator) {
    indicatorActions_1.default.remove(indicator);
}
exports.removeIndicator = removeIndicator;
// Clears all indicators
function clearIndicators() {
    indicatorActions_1.default.clear();
}
exports.clearIndicators = clearIndicators;
// Note previous IndicatorStore.add behavior was to default to "loading" if no type was supplied
function addMessage(msg, type, options = {}) {
    const { duration: optionsDuration, append } = options, rest = (0, tslib_1.__rest)(options, ["duration", "append"]);
    // XXX: Debug for https://sentry.io/organizations/sentry/issues/1595204979/
    if (
    // @ts-expect-error
    typeof (msg === null || msg === void 0 ? void 0 : msg.message) !== 'undefined' &&
        // @ts-expect-error
        typeof (msg === null || msg === void 0 ? void 0 : msg.code) !== 'undefined' &&
        // @ts-expect-error
        typeof (msg === null || msg === void 0 ? void 0 : msg.extra) !== 'undefined') {
        Sentry.captureException(new Error('Attempt to XHR response to Indicators'));
    }
    // use default only if undefined, as 0 is a valid duration
    const duration = typeof optionsDuration === 'undefined' ? constants_1.DEFAULT_TOAST_DURATION : optionsDuration;
    const action = append ? 'append' : 'replace';
    // XXX: This differs from `IndicatorStore.add` since it won't return the indicator that is created
    // because we are firing an action. You can just add a new message and it will, by default,
    // replace active indicator
    indicatorActions_1.default[action](msg, type, Object.assign(Object.assign({}, rest), { duration }));
}
exports.addMessage = addMessage;
function addMessageWithType(type) {
    return (msg, options) => addMessage(msg, type, options);
}
function addLoadingMessage(msg = (0, locale_1.t)('Saving changes...'), options) {
    return addMessageWithType('loading')(msg, options);
}
exports.addLoadingMessage = addLoadingMessage;
function addErrorMessage(msg, options) {
    return addMessageWithType('error')(msg, options);
}
exports.addErrorMessage = addErrorMessage;
function addSuccessMessage(msg, options) {
    return addMessageWithType('success')(msg, options);
}
exports.addSuccessMessage = addSuccessMessage;
const PRETTY_VALUES = new Map([
    ['', '<empty>'],
    [null, '<none>'],
    [undefined, '<unset>'],
    // if we don't cast as any, then typescript complains because booleans are not valid keys
    [true, 'enabled'],
    [false, 'disabled'],
]);
// Transform form values into a string
// Otherwise bool values will not get rendered and empty strings look like a bug
const prettyFormString = (val, model, fieldName) => {
    const descriptor = model.fieldDescriptor.get(fieldName);
    if (descriptor && typeof descriptor.formatMessageValue === 'function') {
        const initialData = model.initialData;
        // XXX(epurkhsier): We pass the "props" as the descriptor and initialData.
        // This isn't necessarily all of the props of the form field, but should
        // make up a good portion needed for formatting.
        return descriptor.formatMessageValue(val, Object.assign(Object.assign({}, descriptor), { initialData }));
    }
    if (PRETTY_VALUES.has(val)) {
        return PRETTY_VALUES.get(val);
    }
    return typeof val === 'object' ? val : String(val);
};
/**
 * This will call an action creator to generate a "Toast" message that
 * notifies user the field that changed with its previous and current values.
 *
 * Also allows for undo
 */
function saveOnBlurUndoMessage(change, model, fieldName) {
    if (!model) {
        return;
    }
    const label = model.getDescriptor(fieldName, 'label');
    if (!label) {
        return;
    }
    const prettifyValue = (val) => prettyFormString(val, model, fieldName);
    // Hide the change text when formatMessageValue is explicitly set to false
    const showChangeText = model.getDescriptor(fieldName, 'formatMessageValue') !== false;
    addSuccessMessage((0, locale_1.tct)(showChangeText
        ? 'Changed [fieldName] from [oldValue] to [newValue]'
        : 'Changed [fieldName]', {
        root: <MessageContainer />,
        fieldName: <FieldName>{label}</FieldName>,
        oldValue: <FormValue>{prettifyValue(change.old)}</FormValue>,
        newValue: <FormValue>{prettifyValue(change.new)}</FormValue>,
    }), {
        modelArg: {
            model,
            id: fieldName,
            undo: () => {
                if (!model || !fieldName) {
                    return;
                }
                const oldValue = model.getValue(fieldName);
                const didUndo = model.undo();
                const newValue = model.getValue(fieldName);
                if (!didUndo) {
                    return;
                }
                if (!label) {
                    return;
                }
                // `saveField` can return null if it can't save
                const saveResult = model.saveField(fieldName, newValue);
                if (!saveResult) {
                    addErrorMessage((0, locale_1.tct)(showChangeText
                        ? 'Unable to restore [fieldName] from [oldValue] to [newValue]'
                        : 'Unable to restore [fieldName]', {
                        root: <MessageContainer />,
                        fieldName: <FieldName>{label}</FieldName>,
                        oldValue: <FormValue>{prettifyValue(oldValue)}</FormValue>,
                        newValue: <FormValue>{prettifyValue(newValue)}</FormValue>,
                    }));
                    return;
                }
                saveResult.then(() => {
                    addMessage((0, locale_1.tct)(showChangeText
                        ? 'Restored [fieldName] from [oldValue] to [newValue]'
                        : 'Restored [fieldName]', {
                        root: <MessageContainer />,
                        fieldName: <FieldName>{label}</FieldName>,
                        oldValue: <FormValue>{prettifyValue(oldValue)}</FormValue>,
                        newValue: <FormValue>{prettifyValue(newValue)}</FormValue>,
                    }), 'undo', {
                        duration: constants_1.DEFAULT_TOAST_DURATION,
                    });
                });
            },
        },
    });
}
exports.saveOnBlurUndoMessage = saveOnBlurUndoMessage;
const FormValue = (0, styled_1.default)('span') `
  font-style: italic;
  margin: 0 ${(0, space_1.default)(0.5)};
`;
const FieldName = (0, styled_1.default)('span') `
  font-weight: bold;
  margin: 0 ${(0, space_1.default)(0.5)};
`;
const MessageContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
//# sourceMappingURL=indicator.jsx.map