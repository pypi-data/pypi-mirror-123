Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const internalStatChart_1 = (0, tslib_1.__importDefault)(require("app/components/internalStatChart"));
const AdminBuffer = () => {
    const since = new Date().getTime() / 1000 - 3600 * 24 * 7;
    return (<div>
      <h3>Buffers</h3>

      <div className="box">
        <div className="box-header">
          <h4>About</h4>
        </div>

        <div className="box-content with-padding">
          <p>
            Sentry buffers are responsible for making changes to cardinality counters —
            such as an issues event count — as well as updating attributes like{' '}
            <em>last seen</em>. These are flushed on a regularly interval, and are
            directly affected by the queue backlog.
          </p>
        </div>
      </div>

      <div className="box">
        <div className="box-header">
          <h4>Updates Processed</h4>
        </div>
        <internalStatChart_1.default since={since} resolution="1h" stat="jobs.finished.sentry.tasks.process_buffer.process_incr" label="Jobs"/>
      </div>

      <div className="box">
        <div className="box-header">
          <h4>Revoked Updates</h4>
        </div>
        <internalStatChart_1.default since={since} resolution="1h" stat="buffer.revoked" label="Jobs"/>
      </div>
    </div>);
};
exports.default = AdminBuffer;
//# sourceMappingURL=adminBuffer.jsx.map