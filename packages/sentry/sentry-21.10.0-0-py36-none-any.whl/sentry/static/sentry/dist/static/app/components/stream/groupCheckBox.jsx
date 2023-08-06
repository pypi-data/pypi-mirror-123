Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const locale_1 = require("app/locale");
const selectedGroupStore_1 = (0, tslib_1.__importDefault)(require("app/stores/selectedGroupStore"));
class GroupCheckBox extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isSelected: selectedGroupStore_1.default.isSelected(this.props.id),
        };
        this.unsubscribe = selectedGroupStore_1.default.listen(() => {
            this.onSelectedGroupChange();
        }, undefined);
        this.handleSelect = () => {
            const id = this.props.id;
            selectedGroupStore_1.default.toggleSelect(id);
        };
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                isSelected: selectedGroupStore_1.default.isSelected(nextProps.id),
            });
        }
    }
    shouldComponentUpdate(_nextProps, nextState) {
        return nextState.isSelected !== this.state.isSelected;
    }
    componentWillUnmount() {
        this.unsubscribe();
    }
    onSelectedGroupChange() {
        const isSelected = selectedGroupStore_1.default.isSelected(this.props.id);
        if (isSelected !== this.state.isSelected) {
            this.setState({
                isSelected,
            });
        }
    }
    render() {
        const { disabled, id } = this.props;
        const { isSelected } = this.state;
        return (<checkbox_1.default aria-label={(0, locale_1.t)('Select Issue')} value={id} checked={isSelected} onChange={this.handleSelect} disabled={disabled}/>);
    }
}
exports.default = GroupCheckBox;
//# sourceMappingURL=groupCheckBox.jsx.map