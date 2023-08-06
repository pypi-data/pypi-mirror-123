Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const locale_1 = require("app/locale");
const handleXhrErrorResponse_1 = (0, tslib_1.__importDefault)(require("app/utils/handleXhrErrorResponse"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("./selectControl"));
/**
 * Performs an API request to `url` when menu is initially opened
 */
class SelectAsyncControl extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
        this.doQuery = (0, debounce_1.default)(cb => {
            const { url, onQuery } = this.props;
            const { query } = this.state;
            if (!this.api) {
                return null;
            }
            return this.api
                .requestPromise(url, {
                query: typeof onQuery === 'function' ? onQuery(query) : { query },
            })
                .then(data => cb(null, data), err => cb(err));
        }, 250);
        this.handleLoadOptions = () => new Promise((resolve, reject) => {
            this.doQuery((err, result) => {
                if (err) {
                    reject(err);
                }
                else {
                    resolve(result);
                }
            });
        }).then(resp => {
            const { onResults } = this.props;
            return typeof onResults === 'function' ? onResults(resp) : resp;
        }, err => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was a problem with the request.'));
            (0, handleXhrErrorResponse_1.default)('SelectAsync failed')(err);
            // eslint-disable-next-line no-console
            console.error(err);
        });
        this.handleInputChange = query => {
            this.setState({ query });
        };
        this.api = new api_1.Client();
        this.state = {
            query: '',
        };
        this.cache = {};
    }
    componentWillUnmount() {
        if (!this.api) {
            return;
        }
        this.api.clear();
        this.api = null;
    }
    render() {
        const _a = this.props, { value, forwardedRef } = _a, props = (0, tslib_1.__rest)(_a, ["value", "forwardedRef"]);
        return (<selectControl_1.default 
        // The key is used as a way to force a reload of the options:
        // https://github.com/JedWatson/react-select/issues/1879#issuecomment-316871520
        key={value} ref={forwardedRef} value={value} defaultOptions loadOptions={this.handleLoadOptions} onInputChange={this.handleInputChange} async cache={this.cache} {...props}/>);
    }
}
SelectAsyncControl.defaultProps = {
    placeholder: '--',
};
const forwardRef = (p, ref) => <SelectAsyncControl {...p} forwardedRef={ref}/>;
forwardRef.displayName = 'SelectAsyncControl';
exports.default = React.forwardRef(forwardRef);
//# sourceMappingURL=selectAsyncControl.jsx.map