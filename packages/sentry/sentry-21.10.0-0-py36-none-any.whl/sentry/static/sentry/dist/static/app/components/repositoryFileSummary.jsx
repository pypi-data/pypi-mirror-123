Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const fileChange_1 = (0, tslib_1.__importDefault)(require("app/components/fileChange"));
const listGroup_1 = require("app/components/listGroup");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function Collapsed(props) {
    return (<listGroup_1.ListGroupItem centered>
      <a onClick={props.onClick}>
        {(0, locale_1.tn)('Show %s collapsed file', 'Show %s collapsed files', props.count)}
      </a>
    </listGroup_1.ListGroupItem>);
}
class RepositoryFileSummary extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            collapsed: true,
        };
        this.onCollapseToggle = () => {
            this.setState({
                collapsed: !this.state.collapsed,
            });
        };
    }
    render() {
        const { repository, fileChangeSummary, collapsible, maxWhenCollapsed } = this.props;
        let files = Object.keys(fileChangeSummary);
        const fileCount = files.length;
        files.sort();
        if (this.state.collapsed && collapsible && fileCount > maxWhenCollapsed) {
            files = files.slice(0, maxWhenCollapsed);
        }
        const numCollapsed = fileCount - files.length;
        const canCollapse = collapsible && fileCount > maxWhenCollapsed;
        return (<Container>
        <h5>
          {(0, locale_1.tn)('%s file changed in ' + repository, '%s files changed in ' + repository, fileCount)}
        </h5>
        <listGroup_1.ListGroup striped>
          {files.map(filename => {
                const { authors } = fileChangeSummary[filename];
                return (<fileChange_1.default key={filename} filename={filename} authors={authors ? Object.values(authors) : []}/>);
            })}
          {numCollapsed > 0 && (<Collapsed onClick={this.onCollapseToggle} count={numCollapsed}/>)}
          {numCollapsed === 0 && canCollapse && (<listGroup_1.ListGroupItem centered>
              <a onClick={this.onCollapseToggle}>{(0, locale_1.t)('Collapse')}</a>
            </listGroup_1.ListGroupItem>)}
        </listGroup_1.ListGroup>
      </Container>);
    }
}
RepositoryFileSummary.defaultProps = {
    collapsible: true,
    maxWhenCollapsed: 5,
};
const Container = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
exports.default = RepositoryFileSummary;
//# sourceMappingURL=repositoryFileSummary.jsx.map