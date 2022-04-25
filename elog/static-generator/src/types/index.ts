export type LogRecord = {
  id: number;
  code: number;
  httpmethod: string;
  errormsg: string;
  errortraceback: string;
  errortype: string;
  ip: string;
  postvalues: string;
  referrer: string;
  requestargs: string;
  requestpath: string;
  useragent: string;
  userbrowser: string;
  userbrowserversion: string;
  userplatform: string;
  when: string;
};

