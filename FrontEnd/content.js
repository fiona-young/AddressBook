var app = angular.module('TabsApp', []);
app.controller('TabsCtrl', function($scope, $http) {
    $scope.url={base:'http://127.0.0.1:5000/address/api/v1.0/',people:'people/',companies:'companies/'};
    $scope.ids = {'intro': 'intro', 'companies': 'companies', 'people': 'people'};
    $scope.tabs = [ {
        id: $scope.ids.intro,
        title: 'Introduction'
    },{
        id: $scope.ids.companies,
            title: 'Organisations',
            url: 'organisations.tpl.html'
        }, {
        id: $scope.ids.people,
            title: 'People'
    }];

    $scope.currentId = $scope.ids.intro;
    $scope.onClickTab = function (tab) {
        if($scope.currentId === $scope.ids.companies){
            updateCompanies($scope.companies)
        }
        $scope.currentId = tab.id;
        if(tab.id === $scope.ids.companies){loadCompanies()}
        else if(tab.id === $scope.ids.people){loadPeople()}
    };

    $scope.isActiveTab = function(tabId) {
        return tabId == $scope.currentId;
    };

    $scope.onToggleCompany = function (company) {
        company = getProcessedCompany(company);
        company.edit = !company.edit;
    };

    $scope.onSubmitCompany = function (myForm,companies) {
        if(myForm.$dirty) {
            updateCompanies(companies)
        }
        myForm.$setPristine();
    };

    var updateCompanies= function( companies){
        var data=[];
        angular.forEach(companies, function(company){
            if(company.edit){
                data.push(company)
            }
        });
        if(data.length){
            putCompanies(data)
        }
    };

    var putCompanies = function (data) {
        $http.put($scope.url.base + $scope.url.companies,data)
            .then(function (response) {
                loadCompanies();
            });
    };

    var loadCompanies = function () {
        $http.get($scope.url.base + $scope.url.companies)
            .then(function (response) {
                $scope.companies = $scope.processCompanies(response.data.companies);
            });
    };

    $scope.processCompanies = function(rawCompanies){
        var companies = [];
        angular.forEach(rawCompanies, function(company){
            companies.push(getProcessedCompany(company));
        });
        companies.push({edit:true});
        return companies;
    };

    var getProcessedCompany = function(company){
        company.emailTxt = implode(company.emails);
        company.phoneTxt = implode(company.phones);
        company.addressTxt = getAddress(company);
        if(company.edit===undefined) {
            company.edit = false;
        }
        return company;
    };

    var getAddress= function(company){
        var address = [];
        angular.forEach(['line1','line2','postcode','country'], function(item){
            if(company[item]!==undefined){
                address.push(company[item])
            }
        });
        return address.join("\n");

    };

    var implode = function(object){
        var list=[];
        angular.forEach(object,function(value,key){list.push(value)});
        return list.join("\n");
    };

    var loadPeople = function(){
        debugger;
        $http.get($scope.url.base+$scope.url.people)
            .then(function (response) {$scope.people = response.data.people;
            });
    };

});