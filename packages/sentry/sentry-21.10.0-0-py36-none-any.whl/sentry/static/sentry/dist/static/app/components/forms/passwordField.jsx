Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/inputField"));
const state_1 = (0, tslib_1.__importDefault)(require("app/components/forms/state"));
// TODO(dcramer): im not entirely sure this is working correctly with
// value propagation in all scenarios
class PasswordField extends inputField_1.default {
    constructor(props, context) {
        super(props, context);
        this.cancelEdit = (e) => {
            e.preventDefault();
            this.setState({
                editing: false,
            }, () => {
                this.setValue('');
            });
        };
        this.startEdit = (e) => {
            e.preventDefault();
            this.setState({
                editing: true,
            });
        };
        this.state = Object.assign(Object.assign({}, this.state), { editing: false });
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        // close edit mode after successful save
        // TODO(dcramer): this needs to work with this.context.form
        if (this.props.formState &&
            this.props.formState === state_1.default.SAVING &&
            nextProps.formState === state_1.default.READY) {
            this.setState({
                editing: false,
            });
        }
    }
    getType() {
        return 'password';
    }
    getField() {
        if (!this.props.hasSavedValue) {
            return super.getField();
        }
        if (this.state.editing) {
            return (<div className="form-password editing">
          <div>{super.getField()}</div>
          <div>
            <a onClick={this.cancelEdit}>Cancel</a>
          </div>
        </div>);
        }
        else {
            return (<div className="form-password saved">
          <span>
            {this.props.prefix + new Array(21 - this.props.prefix.length).join('*')}
          </span>
          {!this.props.disabled && <a onClick={this.startEdit}>Edit</a>}
        </div>);
        }
    }
}
exports.default = PasswordField;
PasswordField.defaultProps = Object.assign(Object.assign({}, inputField_1.default.defaultProps), { hasSavedValue: false, prefix: '' });
//# sourceMappingURL=passwordField.jsx.map