Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const debugFiles_1 = require("app/types/debugFiles");
const actions_1 = (0, tslib_1.__importDefault)(require("./actions"));
const details_1 = (0, tslib_1.__importDefault)(require("./details"));
const status_1 = (0, tslib_1.__importDefault)(require("./status"));
const utils_1 = require("./utils");
function Repository({ repository, onDelete, onEdit }) {
    const [isDetailsExpanded, setIsDetailsExpanded] = (0, react_1.useState)(false);
    const { id, name, type } = repository;
    return (<StyledPanelItem>
      <Name>{name}</Name>
      <TypeAndStatus>
        {utils_1.customRepoTypeLabel[type]}
        {repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT && (<status_1.default details={repository.details} onEditRepository={() => onEdit(id)} onRevalidateItunesSession={() => onEdit(id, true)}/>)}
      </TypeAndStatus>
      <actions_1.default repositoryName={name} repositoryType={type} onDelete={() => onDelete(id)} onEdit={() => onEdit(id)} showDetails={repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT} isDetailsDisabled={repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT &&
            repository.details === undefined} isDetailsExpanded={isDetailsExpanded} onToggleDetails={() => setIsDetailsExpanded(!isDetailsExpanded)}/>
      {repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT && isDetailsExpanded && (<details_1.default details={repository.details}/>)}
    </StyledPanelItem>);
}
exports.default = Repository;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: grid;
  grid-template-columns: 1fr;
  row-gap: ${(0, space_1.default)(1)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr max-content;
    grid-template-rows: repeat(2, max-content);
  }
`;
const Name = (0, styled_1.default)('div') `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-row: 1 / 2;
  }
`;
const TypeAndStatus = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray400};
  font-size: ${p => p.theme.fontSizeMedium};
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
  align-items: center;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: max-content minmax(200px, max-content);
    grid-row: 2 / 3;
    grid-gap: ${(0, space_1.default)(1)};
  }
`;
//# sourceMappingURL=repository.jsx.map