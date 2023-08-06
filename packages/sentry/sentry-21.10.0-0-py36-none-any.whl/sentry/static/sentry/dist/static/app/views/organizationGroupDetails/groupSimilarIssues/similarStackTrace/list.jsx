Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const similarSpectrum_1 = (0, tslib_1.__importDefault)(require("app/components/similarSpectrum"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const toolbar_1 = (0, tslib_1.__importDefault)(require("./toolbar"));
class List extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showAllItems: false,
        };
        this.renderEmpty = () => (<panels_1.Panel>
      <panels_1.PanelBody>
        <emptyStateWarning_1.default small withIcon={false}>
          {(0, locale_1.t)('No issues with a similar stack trace have been found.')}
        </emptyStateWarning_1.default>
      </panels_1.PanelBody>
    </panels_1.Panel>);
        this.handleShowAll = () => {
            this.setState({ showAllItems: true });
        };
    }
    render() {
        const { orgId, groupId, project, items, filteredItems, pageLinks, onMerge, v2 } = this.props;
        const { showAllItems } = this.state;
        const hasHiddenItems = !!filteredItems.length;
        const hasResults = items.length > 0 || hasHiddenItems;
        const itemsWithFiltered = items.concat((showAllItems && filteredItems) || []);
        if (!hasResults) {
            return this.renderEmpty();
        }
        return (<react_1.Fragment>
        <Header>
          <similarSpectrum_1.default />
        </Header>

        <panels_1.Panel>
          <toolbar_1.default v2={v2} onMerge={onMerge}/>

          <panels_1.PanelBody>
            {itemsWithFiltered.map(item => (<item_1.default key={item.issue.id} orgId={orgId} v2={v2} groupId={groupId} project={project} {...item}/>))}

            {hasHiddenItems && !showAllItems && (<Footer>
                <button_1.default onClick={this.handleShowAll}>
                  {(0, locale_1.t)('Show %s issues below threshold', filteredItems.length)}
                </button_1.default>
              </Footer>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={pageLinks}/>
      </react_1.Fragment>);
    }
}
List.defaultProps = {
    filteredItems: [],
};
exports.default = List;
const Header = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const Footer = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  padding: ${(0, space_1.default)(1.5)};
`;
//# sourceMappingURL=list.jsx.map