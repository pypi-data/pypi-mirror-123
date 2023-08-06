Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const groupingComponent_1 = require("./groupingComponent");
class GroupingComponentFrames extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            collapsed: true,
        };
    }
    render() {
        const { items, maxVisibleItems } = this.props;
        const { collapsed } = this.state;
        const isCollapsible = items.length > maxVisibleItems;
        return (<React.Fragment>
        {items.map((item, index) => {
                if (!collapsed || index < maxVisibleItems) {
                    return (<groupingComponent_1.GroupingComponentListItem isCollapsible={isCollapsible} key={index}>
                {item}
              </groupingComponent_1.GroupingComponentListItem>);
                }
                if (index === maxVisibleItems) {
                    return (<groupingComponent_1.GroupingComponentListItem key={index}>
                <ToggleCollapse size="small" priority="link" icon={<icons_1.IconAdd size="8px"/>} onClick={() => this.setState({ collapsed: false })}>
                  {(0, locale_1.tct)('show [numberOfFrames] similiar', {
                            numberOfFrames: items.length - maxVisibleItems,
                        })}
                </ToggleCollapse>
              </groupingComponent_1.GroupingComponentListItem>);
                }
                return null;
            })}

        {!collapsed && items.length > maxVisibleItems && (<groupingComponent_1.GroupingComponentListItem>
            <ToggleCollapse size="small" priority="link" icon={<icons_1.IconSubtract size="8px"/>} onClick={() => this.setState({ collapsed: true })}>
              {(0, locale_1.tct)('collapse [numberOfFrames] similiar', {
                    numberOfFrames: items.length - maxVisibleItems,
                })}
            </ToggleCollapse>
          </groupingComponent_1.GroupingComponentListItem>)}
      </React.Fragment>);
    }
}
GroupingComponentFrames.defaultProps = {
    maxVisibleItems: 2,
};
const ToggleCollapse = (0, styled_1.default)(button_1.default) `
  margin: ${(0, space_1.default)(0.5)} 0;
  color: ${p => p.theme.linkColor};
`;
exports.default = GroupingComponentFrames;
//# sourceMappingURL=groupingComponentFrames.jsx.map