Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const input_1 = (0, tslib_1.__importDefault)(require("app/components/activity/note/input"));
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const defaultProps = {
    /**
     * Triggered when local storage has been loaded and parsed.
     */
    onLoad: (data) => data,
    onSave: (data) => data,
};
class NoteInputWithStorage extends React.Component {
    constructor() {
        super(...arguments);
        this.save = (0, debounce_1.default)(value => {
            const { itemKey, onSave } = this.props;
            const currentObj = this.fetchFromStorage() || {};
            this.saveToStorage(Object.assign(Object.assign({}, currentObj), { [itemKey]: onSave(value) }));
        }, 150);
        this.handleChange = (e, options = {}) => {
            const { onChange } = this.props;
            if (onChange) {
                onChange(e, options);
            }
            if (options.updating) {
                return;
            }
            this.save(e.target.value);
        };
        /**
         * Handler when note is created.
         *
         * Remove in progress item from local storage if it exists
         */
        this.handleCreate = (data) => {
            const { itemKey, onCreate } = this.props;
            if (onCreate) {
                onCreate(data);
            }
            // Remove from local storage
            const storageObj = this.fetchFromStorage() || {};
            // Nothing from this `itemKey` is saved to storage, do nothing
            if (!storageObj.hasOwnProperty(itemKey)) {
                return;
            }
            // Remove `itemKey` from stored object and save to storage
            // eslint-disable-next-line no-unused-vars
            const _a = storageObj, _b = itemKey, _oldItem = _a[_b], newStorageObj = (0, tslib_1.__rest)(_a, [typeof _b === "symbol" ? _b : _b + ""]);
            this.saveToStorage(newStorageObj);
        };
    }
    fetchFromStorage() {
        const { storageKey } = this.props;
        const storage = localStorage_1.default.getItem(storageKey);
        if (!storage) {
            return null;
        }
        try {
            return JSON.parse(storage);
        }
        catch (err) {
            Sentry.withScope(scope => {
                scope.setExtra('storage', storage);
                Sentry.captureException(err);
            });
            return null;
        }
    }
    saveToStorage(obj) {
        const { storageKey } = this.props;
        try {
            localStorage_1.default.setItem(storageKey, JSON.stringify(obj));
        }
        catch (err) {
            Sentry.captureException(err);
            Sentry.withScope(scope => {
                scope.setExtra('storage', obj);
                Sentry.captureException(err);
            });
        }
    }
    getValue() {
        const { itemKey, text, onLoad } = this.props;
        if (text) {
            return text;
        }
        const storageObj = this.fetchFromStorage();
        if (!storageObj) {
            return '';
        }
        if (!storageObj.hasOwnProperty(itemKey)) {
            return '';
        }
        if (!onLoad) {
            return storageObj[itemKey];
        }
        return onLoad(storageObj[itemKey]);
    }
    render() {
        // Make sure `this.props` does not override `onChange` and `onCreate`
        return (<input_1.default {...this.props} text={this.getValue()} onCreate={this.handleCreate} onChange={this.handleChange}/>);
    }
}
NoteInputWithStorage.defaultProps = defaultProps;
exports.default = NoteInputWithStorage;
//# sourceMappingURL=inputWithStorage.jsx.map