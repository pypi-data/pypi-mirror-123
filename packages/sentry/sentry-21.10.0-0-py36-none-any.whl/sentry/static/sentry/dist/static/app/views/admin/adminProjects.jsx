Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const resultGrid_1 = (0, tslib_1.__importDefault)(require("app/components/resultGrid"));
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class AdminProjects extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.getRow = (row) => [
            <td key="name">
      <strong>
        <a href={`/${row.organization.slug}/${row.slug}/`}>{row.name}</a>
      </strong>
      <br />
      <small>{row.organization.name}</small>
    </td>,
            <td key="status" style={{ textAlign: 'center' }}>
      {row.status}
    </td>,
            <td key="dateCreated" style={{ textAlign: 'right' }}>
      {(0, moment_1.default)(row.dateCreated).format('ll')}
    </td>,
        ];
    }
    render() {
        const columns = [
            <th key="name">Project</th>,
            <th key="status" style={{ width: 150, textAlign: 'center' }}>
        Status
      </th>,
            <th key="dateCreated" style={{ width: 200, textAlign: 'right' }}>
        Created
      </th>,
        ];
        return (<div>
        <h3>{(0, locale_1.t)('Projects')}</h3>
        <resultGrid_1.default path="/manage/projects/" endpoint="/projects/?show=all" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch filters={{
                status: {
                    name: 'Status',
                    options: [
                        ['active', 'Active'],
                        ['deleted', 'Deleted'],
                    ],
                },
            }} sortOptions={[['date', 'Date Created']]} defaultSort="date" {...this.props}/>
      </div>);
    }
}
exports.default = AdminProjects;
//# sourceMappingURL=adminProjects.jsx.map