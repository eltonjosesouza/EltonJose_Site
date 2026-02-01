/** @type {import('next').NextConfig} */

const {withContentlayer} = require("next-contentlayer")

const nextConfig = {
    output: 'standalone',
    swcMinify: false,
    compiler:{
        removeConsole: true,
    }
};

module.exports = withContentlayer({ ...nextConfig });
