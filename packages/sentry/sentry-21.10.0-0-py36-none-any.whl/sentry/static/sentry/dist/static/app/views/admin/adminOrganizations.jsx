Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const resultGrid_1 = (0, tslib_1.__importDefault)(require("app/components/resultGrid"));
const locale_1 = require("app/locale");
const getRow = (row) => [
    <td key={row.id}>
    <strong>
      <link_1.default to={`/${row.slug}/`}>{row.name}</link_1.default>
    </strong>
    <br />
    <small>{row.slug}</small>
  </td>,
];
const AdminOrganizations = (props) => (<div>
    <h3>{(0, locale_1.t)('Organizations')}</h3>
    <resultGrid_1.default path="/manage/organizations/" endpoint="/organizations/?show=all" method="GET" columns={[<th key="column-org">Organization</th>]} columnsForRow={getRow} hasSearch sortOptions={[
        ['date', 'Date Joined'],
        ['members', 'Members'],
        ['events', 'Events'],
        ['projects', 'Projects'],
        ['employees', 'Employees'],
    ]} defaultSort="date" {...props}/>
  </div>);
exports.default = AdminOrganizations;
//# sourceMappingURL=adminOrganizations.jsx.map