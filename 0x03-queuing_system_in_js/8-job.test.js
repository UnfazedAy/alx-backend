import createPushNotificationsJobs from "./8-job";
import { createQueue } from 'kue';
import { expect } from 'chai';
import assert from 'assert';
import sinon from 'sinon';

const queue = createQueue();

describe('createPushNotificationsJobs', function() {
  let consoleLogSpy;

  beforeEach(() => consoleLogSpy = sinon.spy(console, 'log'));
  afterEach(() => consoleLogSpy.restore());
  before(() => queue.testMode.enter());
  after(() => queue.testMode.clear());
  after(() => queue.testMode.exit());

  it('should throw an error if jobs is not an array', (done) => {
    expect(() => createPushNotificationsJobs('Author is Ayomide', queue)).to.throw('Jobs is not an array');
    done();
  });

  it('should create a job for each data in the job object', (done) => {
    const jobs = [
        { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
        { phoneNumber: '4153518781', message: 'This is the code 5678 to verify your account' }
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(jobs.length);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    queue.process('push_notification_code_3', () => {
      assert(consoleLogSpy.calledWithExactly('Notification job created:', queue.testMode.jobs[0].id));
    });
    done();
  });
});