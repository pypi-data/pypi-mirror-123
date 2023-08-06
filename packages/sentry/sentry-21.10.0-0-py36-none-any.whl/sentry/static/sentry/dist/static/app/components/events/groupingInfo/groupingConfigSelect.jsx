Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const _1 = require(".");
class GroupingConfigSelect extends asyncComponent_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { configs: [] });
    }
    getEndpoints() {
        return [['configs', '/grouping-configs/']];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { configId, eventConfigId, onSelect } = this.props;
        const { configs } = this.state;
        const options = configs.map(({ id, hidden }) => ({
            value: id,
            label: (<_1.GroupingConfigItem isHidden={hidden} isActive={id === eventConfigId}>
          {id}
        </_1.GroupingConfigItem>),
        }));
        return (<dropdownAutoComplete_1.default onSelect={onSelect} items={options}>
        {({ isOpen }) => (<tooltip_1.default title={(0, locale_1.t)('Click here to experiment with other grouping configs')}>
            <StyledDropdownButton isOpen={isOpen} size="small">
              <_1.GroupingConfigItem isActive={eventConfigId === configId}>
                {configId}
              </_1.GroupingConfigItem>
            </StyledDropdownButton>
          </tooltip_1.default>)}
      </dropdownAutoComplete_1.default>);
    }
}
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  font-weight: inherit;
`;
exports.default = GroupingConfigSelect;
//# sourceMappingURL=groupingConfigSelect.jsx.map