Object.defineProperty(exports, "__esModule", { value: true });
exports.prettyDate = void 0;
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const resultGrid_1 = (0, tslib_1.__importDefault)(require("app/components/resultGrid"));
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const prettyDate = function (x) {
    return (0, moment_1.default)(x).format('ll');
};
exports.prettyDate = prettyDate;
class AdminUsers extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.getRow = (row) => [
            <td key="username">
      <strong>
        <link_1.default to={`/manage/users/${row.id}/`}>{row.username}</link_1.default>
      </strong>
      <br />
      {row.email !== row.username && <small>{row.email}</small>}
    </td>,
            <td key="dateJoined" style={{ textAlign: 'center' }}>
      {(0, exports.prettyDate)(row.dateJoined)}
    </td>,
            <td key="lastLogin" style={{ textAlign: 'center' }}>
      {(0, exports.prettyDate)(row.lastLogin)}
    </td>,
        ];
    }
    render() {
        const columns = [
            <th key="username">User</th>,
            <th key="dateJoined" style={{ textAlign: 'center', width: 150 }}>
        Joined
      </th>,
            <th key="lastLogin" style={{ textAlign: 'center', width: 150 }}>
        Last Login
      </th>,
        ];
        return (<div>
        <h3>{(0, locale_1.t)('Users')}</h3>
        <resultGrid_1.default path="/manage/users/" endpoint="/users/" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch filters={{
                status: {
                    name: 'Status',
                    options: [
                        ['active', 'Active'],
                        ['disabled', 'Disabled'],
                    ],
                },
            }} sortOptions={[['date', 'Date Joined']]} defaultSort="date" {...this.props}/>
      </div>);
    }
}
exports.default = AdminUsers;
//# sourceMappingURL=adminUsers.jsx.map