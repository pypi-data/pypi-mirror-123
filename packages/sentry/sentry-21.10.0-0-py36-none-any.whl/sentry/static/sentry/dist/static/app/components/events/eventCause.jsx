Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const flatMap_1 = (0, tslib_1.__importDefault)(require("lodash/flatMap"));
const uniqBy_1 = (0, tslib_1.__importDefault)(require("lodash/uniqBy"));
const commitRow_1 = (0, tslib_1.__importDefault)(require("app/components/commitRow"));
const styles_1 = require("app/components/events/styles");
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withCommitters_1 = (0, tslib_1.__importDefault)(require("app/utils/withCommitters"));
class EventCause extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            expanded: false,
        };
    }
    getUniqueCommitsWithAuthors() {
        const { committers } = this.props;
        // Get a list of commits with author information attached
        const commitsWithAuthors = (0, flatMap_1.default)(committers, ({ commits, author }) => commits.map(commit => (Object.assign(Object.assign({}, commit), { author }))));
        // Remove duplicate commits
        const uniqueCommitsWithAuthors = (0, uniqBy_1.default)(commitsWithAuthors, commit => commit.id);
        return uniqueCommitsWithAuthors;
    }
    render() {
        const { committers } = this.props;
        const { expanded } = this.state;
        if (!(committers === null || committers === void 0 ? void 0 : committers.length)) {
            return null;
        }
        const commits = this.getUniqueCommitsWithAuthors();
        return (<styles_1.DataSection>
        <styles_1.CauseHeader>
          <h3>
            {(0, locale_1.t)('Suspect Commits')} ({commits.length})
          </h3>
          {commits.length > 1 && (<ExpandButton onClick={() => this.setState({ expanded: !expanded })}>
              {expanded ? (<react_1.Fragment>
                  {(0, locale_1.t)('Show less')} <icons_1.IconSubtract isCircled size="md"/>
                </react_1.Fragment>) : (<react_1.Fragment>
                  {(0, locale_1.t)('Show more')} <icons_1.IconAdd isCircled size="md"/>
                </react_1.Fragment>)}
            </ExpandButton>)}
        </styles_1.CauseHeader>
        <panels_1.Panel>
          {commits.slice(0, expanded ? 100 : 1).map(commit => (<commitRow_1.default key={commit.id} commit={commit}/>))}
        </panels_1.Panel>
      </styles_1.DataSection>);
    }
}
const ExpandButton = (0, styled_1.default)('button') `
  display: flex;
  align-items: center;
  & > svg {
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
exports.default = (0, withApi_1.default)((0, withCommitters_1.default)(EventCause));
//# sourceMappingURL=eventCause.jsx.map